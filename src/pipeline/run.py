"""pipeline/run.py — minimal stage-based CLI orchestrator (M2).

Stages: preprocess | langid | sentiment | stance | framing.
Each stage runs independently over an explicit input CSV and writes an
explicit output CSV plus a stage manifest (<output>.manifest.json).

Contract (M2):
  - post_id is the record join key and must be present and unique.
  - No records are dropped or added; no default labels are created.
  - Failures are loud: invalid stage/input/schema -> non-zero exit, and a
    manifest with status="failed" whenever an output path is resolvable.
  - Inputs are never overwritten; outputs are written atomically (tmp+replace).
  - No new transformations: every stage delegates to the audited functions in
    src/nlp_core.py / src/pipeline/*, mirroring the per-platform semantics of
    the authoritative builder (news framing/rule on full_text; X/YT on
    clean_text; langid via API lang for X, langdetect otherwise).

The sentiment stage requires a torch/transformers environment. Without one it
fails loudly and reports clearly — it never simulates successful execution.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from config_loader import (  # noqa: E402
    content_version, load_models_config, load_pipeline_config)
from pipeline import framing as framing_mod  # noqa: E402
from pipeline import langid as langid_mod  # noqa: E402
from pipeline import preprocess as prep_mod  # noqa: E402
from pipeline import stance as stance_mod  # noqa: E402

STAGES = ["preprocess", "langid", "sentiment", "stance", "framing"]
PLATFORMS = ["x", "youtube", "news"]
PLATFORM_VARIANT = {"x": "x_v2", "youtube": "youtube", "news": "news"}
MANIFEST_SCHEMA = "stage-manifest-v1"


class StageError(Exception):
    """Raised for any invalid input, schema violation, or stage failure."""


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _core_stance_passthrough_keys(variant: str):
    import nlp_core as _nc
    return _nc.STANCE_RULES[variant]["passthrough"].keys()


def _versions(model_version: str | None = None) -> dict:
    """T3: actual version/configuration identifiers (never invented)."""
    return {
        "pipeline_version": load_pipeline_config()["pipeline_version"],
        "lexicon_version": content_version("lexicon.yaml"),
        "rules_version": content_version("rules.yaml"),
        "model_version": model_version or load_models_config()["sentiment"].get("revision", "unknown"),
    }


def _git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=_SRC, capture_output=True, text=True)
        return out.stdout.strip() or "unknown (no git)"
    except Exception:
        return "unknown (no git)"


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_table(path: str) -> pd.DataFrame:
    if not os.path.isfile(path):
        raise StageError(f"input file not found: {path}")
    try:
        df = pd.read_csv(path, encoding="utf-8-sig", dtype={"post_id": str})
    except Exception as e:
        raise StageError(f"input is not a readable CSV ({path}): {e}") from e
    if df.empty:
        raise StageError(f"input contains no records: {path}")
    return df


def _require_columns(df: pd.DataFrame, required: list, path: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise StageError(f"input {path} is missing required column(s): {missing}")


def _require_unique_post_id(df: pd.DataFrame, path: str) -> None:
    if "post_id" not in df.columns:
        raise StageError(f"input {path} is missing the 'post_id' join key")
    dups = int(df["post_id"].duplicated().sum())
    if dups:
        raise StageError(
            f"input {path} contains {dups} duplicate post_id values; the data "
            "contract requires post_id to be unique (deduplicate upstream, "
            "do not rely on the stage to drop records)")


def _stage_text(df: pd.DataFrame, platform: str) -> pd.Series:
    """Text input per existing per-platform semantics: news -> full_text;
    x/youtube -> clean_text (computed via the existing cleaning if absent)."""
    if platform == "news":
        return df["full_text"].fillna("").astype(str)
    if "clean_text" in df.columns:
        return df["clean_text"].fillna("").astype(str)
    return df["full_text"].fillna("").astype(str).map(prep_mod.clean_for_lexicon)


def _atomic_write_csv(df: pd.DataFrame, path: str) -> None:
    tmp = path + ".tmp"
    df.to_csv(tmp, index=False, encoding="utf-8-sig", lineterminator="\n")
    os.replace(tmp, path)


def _write_manifest(path: str, manifest: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True, ensure_ascii=False)


def run_stage(stage: str, platform: str, input_path: str, output_path: str,
              variant: str | None = None) -> dict:
    """Execute one stage. Returns the stage manifest (status ok/failed).
    Raises StageError for invalid arguments; runtime stage failures are
    recorded in the manifest with status='failed' and re-raised."""
    if stage not in STAGES:
        raise StageError(f"invalid stage: {stage!r} (available: {STAGES})")
    if platform not in PLATFORMS:
        raise StageError(f"invalid platform: {platform!r} (available: {PLATFORMS})")
    if not input_path or not output_path:
        raise StageError("both --input and --output paths are required")
    if os.path.abspath(input_path) == os.path.abspath(output_path):
        raise StageError("output path must differ from input path (inputs are never overwritten)")

    manifest = {
        "schema": MANIFEST_SCHEMA, "stage": stage, "platform": platform,
        "variant": variant if stage == "stance" else None,
        "input": {"path": input_path}, "output": None,
        "status": "failed", "error": None,
        "started_utc": _now_utc(), "finished_utc": None,
        "code_commit": _git_commit(),
        "versions": _versions(),
    }
    manifest_path = output_path + ".manifest.json"
    # T2.1: invalidate any previous artifact at the output path — a failed run
    # must never leave a stale successful CSV next to a "failed" manifest.
    for stale in (output_path, manifest_path):
        if os.path.exists(stale):
            try:
                os.remove(stale)
            except OSError as e:
                raise StageError(f"cannot remove previous artifact {stale}: {e}") from e
    try:
        df = _load_table(input_path)
        _require_columns(df, ["full_text"], input_path)
        _require_unique_post_id(df, input_path)
        manifest["input"]["sha256"] = _sha256(input_path)
        manifest["input"]["rows"] = int(len(df))
        rows_in = len(df)

        out = df.copy()
        if stage == "preprocess":
            out["clean_text"] = out["full_text"].fillna("").astype(str).map(prep_mod.clean_for_lexicon)
            if platform == "news":
                out["clean_lead"] = out["full_text"].fillna("").astype(str).map(prep_mod.extract_lead_text)
        elif stage == "langid":
            if platform == "x":
                _require_columns(df, ["language"], input_path)
                out["language"] = out["language"].map(langid_mod.normalize_x_language)
                out["language_source"] = "x_api_lang_normalized"
            else:
                out["language"] = out["full_text"].fillna("").astype(str).map(langid_mod.detect_language)
                out["language_source"] = "langdetect_seed0"
        elif stage == "sentiment":
            _require_columns(df, ["language"], input_path)
            # Sentiment stage requires the model environment; it fails loudly
            # rather than simulating execution (no default labels, ever).
            from pipeline import sentiment as sentiment_mod
            langs = out["language"].astype(str).tolist()
            mask = sentiment_mod.english_only_mask(langs)
            tok, model, device = sentiment_mod.load_model()  # raises SentimentError loudly
            manifest["versions"]["model_version"] = sentiment_mod.resolved_model_version(model)
            texts = [sentiment_mod.model_card_preprocess(t) if keep else ""
                     for t, keep in zip(out["full_text"].fillna("").astype(str), mask)]
            preds = sentiment_mod.predict(texts, tok, model, device)
            labels = [p[0] if keep else None for p, keep in zip(preds, mask)]
            scores = [p[1] if keep else None for p, keep in zip(preds, mask)]
            out["sentiment_model"] = labels
            out["sentiment_model_score"] = scores
            out["sentiment_guard"] = ["en_inferred" if k else "skipped_non_english" for k in mask]
        elif stage == "stance":
            var = variant or PLATFORM_VARIANT[platform]
            if var not in stance_mod.VARIANTS:
                raise StageError(f"unknown stance variant: {var!r} (available: {stance_mod.VARIANTS})")
            manifest["variant"] = var
            text_col = _stage_text(df, platform)
            base_col = out["sentiment_model"] if "sentiment_model" in out.columns else None
            # T2.3: strict base-label vocabulary guard. The rule layer's
            # passthrough maps are platform-native; feeding unified English
            # labels (e.g. 'Negative') would silently leak the wrong
            # vocabulary into stance_rule_adjusted. Fail loudly instead.
            if base_col is not None:
                allowed = set(_core_stance_passthrough_keys(var)) | {""}
                present = {str(b) for b in base_col.dropna().astype(str) if str(b).strip()}
                incompatible = sorted(present - allowed)
                if incompatible:
                    raise StageError(
                        f"stance base-label vocabulary incompatible with variant '{var}': "
                        f"{incompatible[:5]}{'...' if len(incompatible) > 5 else ''} "
                        f"(allowed: {sorted(a for a in allowed if a)}). Provide platform-native "
                        f"base labels matching the variant passthrough keys, or omit the "
                        f"sentiment_model column to run the rule layer without a base label.")
            adj, ev, fired = [], [], []
            for i, t in enumerate(text_col):
                base = str(base_col.iloc[i]) if base_col is not None and pd.notna(base_col.iloc[i]) else ""
                label, evidence, hit = stance_mod.apply_stance_rule(t, base, var)
                adj.append(label if (hit or base) else None)  # unknown base + no fire = undetermined, not a default label
                ev.append(";".join(evidence))
                fired.append(bool(hit))
            out["stance_rule_adjusted"] = adj
            out["stance_rule_evidence"] = ev
            out["stance_rule_fired"] = fired
        elif stage == "framing":
            text_col = _stage_text(df, platform)
            frames, evidences = [], []
            for t in text_col:
                frame, _, evidence = framing_mod.classify_framing(t)
                frames.append(frame)
                evidences.append(";".join(evidence))
            out["thematic_frame"] = frames
            out["framing_evidence"] = evidences

        if len(out) != rows_in:
            raise StageError(f"record count changed during stage: {rows_in} -> {len(out)} (silent loss is forbidden)")
        out_dir = os.path.dirname(os.path.abspath(output_path))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        _atomic_write_csv(out, output_path)
        manifest["output"] = {"path": output_path, "sha256": _sha256(output_path), "rows": int(len(out))}
        manifest["status"] = "ok"
    except Exception as e:  # loud failure with an auditable failed manifest
        # T2.2: failed-run manifests MUST carry finished_utc (including this
        # exception path), so the written file is complete before re-raise.
        manifest["error"] = f"{type(e).__name__}: {e}"
        manifest["finished_utc"] = _now_utc()
        try:
            _write_manifest(manifest_path, manifest)
        except Exception:
            pass
        raise
    manifest["finished_utc"] = _now_utc()
    _write_manifest(manifest_path, manifest)
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="M2 stage-based NLP pipeline orchestrator")
    ap.add_argument("--stage", required=True, choices=STAGES)
    ap.add_argument("--platform", required=True, choices=PLATFORMS,
                    help="x | youtube | news (determines stage semantics)")
    ap.add_argument("--input", required=True, help="input CSV path (never overwritten)")
    ap.add_argument("--output", required=True, help="output CSV path (must differ from input)")
    ap.add_argument("--variant", choices=None, default=None,
                    help="stance stage only: override the platform-default rule variant")
    args = ap.parse_args(argv)
    try:
        manifest = run_stage(args.stage, args.platform, args.input, args.output, args.variant)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        return 1
    print(f"[ok] stage={manifest['stage']} rows={manifest['output']['rows']} "
          f"output={manifest['output']['path']} manifest={manifest['output']['path']}.manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
