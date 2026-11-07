"""run_fresh_inference.py — T1: fresh English-only inference over the retained corpus.

Runs the approved Cardiff model (configs/models.yaml) over ALL retained
English-language records of the repaired master and writes a SEPARATE
refresh artifact (it does NOT modify the production master or the M0 golden
baseline — those remain frozen; merging fresh labels into the master is a
team-approved future step that supersedes the golden baseline).

Verification built in (script completion alone is NOT sufficient):
  - exact target count enforced (1,013 EN records; fails loudly otherwise),
  - every record receives a label from the configured label set,
  - scores within (0, 1],
  - non-degenerate output (more than one distinct label),
  - determinism spot-check (first 10 records re-predicted identically),
  - actual resolved model revision recorded (Hugging Face commit hash).

Usage (in an environment with torch+transformers, e.g. the Python 3.11 venv):
    <venv-python> src/run_fresh_inference.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pipeline import sentiment as sm  # noqa: E402
from config_loader import load_models_config, load_pipeline_config  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MASTER = os.path.join(ROOT, "data", "processed", "master_triangulation_repaired.csv")
REGISTER = os.path.join(ROOT, "docs", "DATA_EXCLUSION_REGISTER.csv")
OUT_CSV = os.path.join(ROOT, "data", "processed", "fresh_inference_en.csv")
OUT_MANIFEST = OUT_CSV + ".manifest.json"
TARGET_LANG = "en"
EXPECTED_TARGET = 1013  # measured in the M2.1 data-quality audit; do not silently reduce


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def die(msg: str) -> None:
    print(f"[FATAL] {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    t0 = time.time()
    pipe_version = load_pipeline_config()["pipeline_version"]
    registry_revision = load_models_config()["sentiment"]["revision"]

    # --- population: retained EN records, exact target enforced ---
    master = pd.read_csv(MASTER, encoding="utf-8-sig", dtype={"post_id": str})
    reg = pd.read_csv(REGISTER, encoding="utf-8")
    excluded = set(reg[reg["dataset"] == "master_repaired"]["post_id"])
    ret = master[~master["post_id"].isin(excluded)]
    en = ret[ret["language"] == TARGET_LANG].sort_values("post_id").reset_index(drop=True)
    if len(en) != EXPECTED_TARGET:
        die(f"EN inference target is {EXPECTED_TARGET} but retained master has {len(en)} "
            f"'{TARGET_LANG}' rows. Do not silently reduce the inference target; "
            "investigate the difference first.")
    print(f"[t1] target population: {len(en)} EN retained records")

    # --- model + actual resolved revision ---
    tok, model, device = sm.load_model()
    model_version = sm.resolved_model_version(model)
    print(f"[t1] resolved model_version: {model_version} (registry: {registry_revision})")

    # --- inference (per-text loop, M2 semantics; batching remains M3) ---
    texts = [sm.model_card_preprocess(t) for t in en["full_text"].fillna("").astype(str)]
    preds = sm.predict(texts, tok, model, device)

    # --- verification: completion is not enough ---
    labels = [p[0] for p in preds]
    scores = [p[1] for p in preds]
    problems = []
    if len(preds) != len(en):
        problems.append(f"prediction count {len(preds)} != input {len(en)}")
    if not set(labels).issubset(set(sm.LABELS)):
        problems.append(f"labels outside configured set: {set(labels) - set(sm.LABELS)}")
    if not all(0.0 < s <= 1.0 for s in scores):
        problems.append("score outside (0, 1]")
    distinct = sorted(set(labels))
    if len(distinct) < 2:
        problems.append(f"degenerate output: only {distinct} produced")
    # determinism spot-check: re-predict the first 10 records
    re_preds = sm.predict(texts[:10], tok, model, device)
    if re_preds != preds[:10]:
        problems.append("determinism spot-check failed on first 10 records")
    if problems:
        die("verification failed: " + "; ".join(problems))
    print(f"[t1] verification OK: {len(preds)} predictions, labels={distinct}, "
          f"determinism spot-check passed")

    # --- write refresh artifact (separate from the frozen master/golden) ---
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out = pd.DataFrame({
        "post_id": en["post_id"],
        "sentiment_model": labels,
        "sentiment_model_score": scores,
        "inference_source": "fresh_inference",
        "model_version": model_version,
        "pipeline_version": pipe_version,
        "inferred_at_utc": stamp,
    })
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig", lineterminator="\n")

    dist = {k: int(v) for k, v in pd.Series(labels).value_counts().items()}
    manifest = {
        "schema": "fresh-inference-manifest-v1",
        "artifact": OUT_CSV,
        "artifact_sha256": sha256(OUT_CSV),
        "rows": int(len(out)),
        "target_language": TARGET_LANG,
        "versions": {
            "pipeline_version": pipe_version,
            "model_name": sm.MODEL_NAME,
            "model_version": model_version,
            "model_revision_registry": registry_revision,
            "lexicon_version": None,  # no lexicon used in sentiment inference
        },
        "environment": {
            "python": sys.version.split()[0],
            "torch": sys.modules["torch"].__version__,
            "transformers": sys.modules["transformers"].__version__,
            "device": device,
        },
        "input": {"master": MASTER, "master_sha256": sha256(MASTER),
                  "golden_baseline_untouched": True},
        "label_distribution": dist,
        "determinism_spot_check": "passed (first 10 records re-predicted identically)",
        "inferred_at_utc": stamp,
        "runtime_seconds": round(time.time() - t0, 1),
        "note": ("Separate refresh artifact: the production master and the M0 golden "
                 "baseline are intentionally NOT modified. Merging these labels into "
                 "the master supersedes the golden baseline and requires team approval."),
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True, ensure_ascii=False)
    print(f"[t1] wrote {OUT_CSV} ({len(out)} rows) + manifest; runtime {manifest['runtime_seconds']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
