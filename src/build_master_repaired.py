"""
build_master_repaired.py — AUTHORITATIVE pipeline for the repaired master dataset.

Regenerates every derived column of the master triangulation dataset using the
repaired logic in nlp_core.py, WITHOUT touching any raw or legacy file.
Transformer re-inference is not executed here (no GPU/transformers in this
environment); rows whose raw model label cannot be recovered from the shipped
legacy outputs are flagged `inference_source='requires_rerun'` instead of being
fabricated (audit AUD-02/AUD-03: no invented labels).

Outputs (new files only; originals preserved):
  data/processed/master_triangulation_repaired.csv
  data/processed/build_manifest.json

Usage (from repo root):  python src/build_master_repaired.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import nlp_core as nc  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "data", "processed")
os.makedirs(OUT_DIR, exist_ok=True)

PATHS = {
    "x_raw": os.path.join(ROOT, "data", "raw", "asean_papua_x_tweets.csv"),
    "yt_raw": os.path.join(ROOT, "data", "raw", "youtube_papua_asean_comments.csv"),
    "news_raw": os.path.join(ROOT, "data", "raw", "news_papua_asean_articles.csv"),
    "x_legacy": os.path.join(ROOT, "archive", "legacy_pipelines", "7_hasil4_x", "asean_papua_sentiment_v2_analyzed.csv"),
    "yt_legacy": os.path.join(ROOT, "archive", "legacy_pipelines", "10_hasil5_yt", "youtube_papua_sentiment_analyzed.csv"),
    "news_legacy": os.path.join(ROOT, "archive", "legacy_pipelines", "13_hasil_news", "news_papua_sentiment_analyzed.csv"),
    "legacy_master": os.path.join(ROOT, "archive", "legacy_pipelines", "14_laporan_dan_master_dataset", "master_triangulation_asean_papua.csv"),
}

# Unified model-label vocabulary for the repaired dataset (platform-native raw
# labels are mapped deterministically; mapping recorded in the manifest).
MODEL_LABEL_MAP = {
    "Positif": "Positive", "Netral": "Neutral", "Negatif": "Negative",
    "positive": "Positive", "neutral": "Neutral", "negative": "Negative",
    "positive ": "Positive", "neutral ": "Neutral", "negative ": "Negative",
}


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def log(msg: str) -> None:
    print(f"[build] {msg}")


# ----------------------------------------------------------------------------
# PLATFORM X
# ----------------------------------------------------------------------------
def build_x() -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(PATHS["x_raw"], encoding="utf-8-sig", dtype={"tweet_id": str})
    legacy = pd.read_csv(PATHS["x_legacy"], encoding="utf-8-sig", dtype={"tweet_id": str})
    leg = legacy.set_index(legacy["tweet_id"].astype(str))

    # --- Reproduce the legacy 427 -> 375 selection deterministically ---
    keep = []
    for _, r in raw.iterrows():
        if nc.is_spam(r.get("username", ""), r.get("full_text", "")):
            continue
        if nc.legacy_is_indonesia_location(r.get("user_location", "")):
            continue
        if not nc.is_relevant_x(r.get("full_text", "")):
            continue
        keep.append(str(r["tweet_id"]))
    legacy_ids = set(leg.index)
    repaired_ids = set(keep)
    diff_out = sorted(legacy_ids - repaired_ids)
    diff_in = sorted(repaired_ids - legacy_ids)

    raw = raw[raw["tweet_id"].astype(str).isin(repaired_ids)].copy()
    log(f"X selection: {len(raw)} rows (legacy={len(legacy_ids)}; "
        f"only-in-legacy={len(diff_out)}; only-in-repaired={len(diff_in)})")

    # Optional refreshed inference (data/processed/model_labels_x_refresh.csv,
    # produced by src/run_inference.py in a torch/transformers env).
    refresh_path = os.path.join(OUT_DIR, "model_labels_x_refresh.csv")
    refresh = None
    if os.path.exists(refresh_path):
        refresh = pd.read_csv(refresh_path, encoding="utf-8-sig", dtype={"post_id": str})
        refresh = refresh.set_index(refresh["post_id"].astype(str))
        log(f"Merging refreshed X inference labels: {len(refresh)} rows "
            f"({int(refresh['sentiment_model'].notna().sum())} with labels)")

    rows = []
    for _, r in raw.iterrows():
        tid = str(r["tweet_id"])
        clean_recomputed = nc.clean_for_lexicon(r.get("full_text", ""))
        legacy_clean = str(leg.at[tid, "clean_text"]) if tid in leg.index else ""
        clean_match = (clean_recomputed == legacy_clean)

        # --- raw model label: recovered where the rule layer did NOT fire ---
        legacy_adj = str(leg.at[tid, "sentiment_v2"]) if tid in leg.index else ""
        legacy_score = leg.at[tid, "sentiment_score"] if tid in leg.index else None
        base_native = nc.recover_x_base_label(legacy_clean, legacy_adj) \
            if tid in leg.index else None
        if base_native is not None:
            model_label, src = MODEL_LABEL_MAP.get(base_native), "legacy_raw_recovered"
            model_score = float(legacy_score) if pd.notna(legacy_score) else None
        else:
            model_label, src, model_score = None, "requires_rerun", None
        # refreshed inference (if available) supersedes legacy-recovery / requires_rerun flags
        if refresh is not None and tid in refresh.index:
            rl = refresh.at[tid, "sentiment_model"]
            rs = refresh.at[tid, "sentiment_model_score"]
            if pd.notna(rl):
                model_label, src = str(rl), "fresh_inference"
                model_score = float(rs) if pd.notna(rs) else None

        # --- rule layer (experimental, separate column, with evidence) ---
        rule_label, evidence, fired = nc.apply_stance_rule(
            legacy_clean, base_native or "", "x_v2")
        if not fired and base_native is None:
            rule_label = None  # passthrough unknown -> do not fabricate

        # --- repaired geo/bloc (origin from profile location ONLY) ---
        origin_country, origin_bloc = nc.origin_from_location(r.get("user_location", ""))
        mentions = nc.topic_country_mentions(r.get("full_text", ""))

        # --- repaired framing (unified lexicon + explicit residual) ---
        frame, _, frame_ev = nc.classify_framing(clean_recomputed)

        rows.append({
            "platform": "Platform X (Twitter)",
            "post_id": tid,
            "created_at": r.get("created_at", ""),
            "created_at_note": "",
            "username": r.get("username", ""),
            "user_location": r.get("user_location", ""),
            "media_source": "X / Twitter Public",
            "url": r.get("tweet_url", ""),
            "language": nc.normalize_x_language(r.get("language", "")),
            "language_source": "x_api_lang_normalized",
            "origin_country": origin_country or "",
            "origin_bloc": origin_bloc,
            "bloc_basis": "profile_location_word_boundary",
            "topic_country_mentions": ";".join(mentions),
            "country_bloc": origin_bloc,
            "full_text": r.get("full_text", ""),
            "clean_text": clean_recomputed,
            "clean_text_matches_legacy": bool(clean_match),
            "sentiment_model": model_label,
            "sentiment_model_score": model_score,
            "inference_source": src,
            "stance_target": nc.STANCE_TARGET,
            "stance_rule_variant": "x_v2",
            "stance_rule_adjusted": rule_label,
            "stance_rule_evidence": ";".join(evidence),
            "stance_rule_fired": fired,
            "legacy_final_label": legacy_adj,
            "thematic_frame": frame,
            "framing_evidence": ";".join(frame_ev),
        })
    stats = {
        "n_selected": len(rows),
        "legacy_ids_not_reproduced": diff_out,
        "repaired_ids_not_in_legacy": diff_in,
        "n_requires_rerun": sum(1 for r in rows if r["inference_source"] == "requires_rerun"),
        "n_legacy_raw_recovered": sum(1 for r in rows if r["inference_source"] == "legacy_raw_recovered"),
    }
    return pd.DataFrame(rows), stats


# ----------------------------------------------------------------------------
# YOUTUBE
# ----------------------------------------------------------------------------
def build_yt() -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(PATHS["yt_raw"], encoding="utf-8-sig", dtype={"post_id": str})
    legacy = pd.read_csv(PATHS["yt_legacy"], encoding="utf-8-sig", dtype={"post_id": str})
    leg = legacy.set_index(legacy["post_id"].astype(str))

    # Reproduce legacy drop rule (empty / <10 chars).
    raw = raw.dropna(subset=["full_text"]).copy()
    raw = raw[raw["full_text"].astype(str).str.strip().str.len() >= 10].copy()
    id_mismatch = set(raw["post_id"]) ^ set(leg.index)

    rows, trace_match = [], 0
    for _, r in raw.iterrows():
        pid = str(r["post_id"])
        clean_recomputed = nc.clean_for_lexicon(r.get("full_text", ""))
        legacy_clean = str(leg.at[pid, "clean_text"]) if pid in leg.index else ""
        clean_match = (clean_recomputed == legacy_clean)

        model_native = str(leg.at[pid, "sentiment_raw"]) if pid in leg.index else ""
        model_score = leg.at[pid, "sentiment_score"] if pid in leg.index else None
        model_label = MODEL_LABEL_MAP.get(model_native)

        # traceability: legacy final label must equal rule(model, legacy_clean)
        trace_label, _, _ = nc.apply_stance_rule(legacy_clean, model_native, "youtube")
        if trace_label == str(leg.at[pid, "sentiment"]):
            trace_match += 1

        # rule layer on recomputed clean text
        rule_label, evidence, fired = nc.apply_stance_rule(
            clean_recomputed, model_native, "youtube")

        frame, _, frame_ev = nc.classify_framing(clean_recomputed)
        lang = nc.detect_language(str(r.get("full_text", "")))

        rows.append({
            "platform": "YouTube Comments",
            "post_id": pid,
            "created_at": r.get("created_at", ""),
            "created_at_note": "relative string from legacy scraper; absolute "
                               "timestamp not available (AUD-08)",
            "username": r.get("username", ""),
            "user_location": r.get("user_location", ""),
            "media_source": r.get("media_source", ""),
            "url": r.get("url", ""),
            "language": lang,
            "language_source": "langdetect_seed0",
            "origin_country": "",
            "origin_bloc": "",
            "bloc_basis": "video_channel_country (commenter origin unknown)",
            "topic_country_mentions": "",
            "country_bloc": r.get("country_bloc", ""),
            "full_text": r.get("full_text", ""),
            "clean_text": clean_recomputed,
            "clean_text_matches_legacy": bool(clean_match),
            "sentiment_model": model_label,
            "sentiment_model_score": float(model_score) if pd.notna(model_score) else None,
            "inference_source": "legacy_raw_recovered",
            "stance_target": nc.STANCE_TARGET,
            "stance_rule_variant": "youtube",
            "stance_rule_adjusted": rule_label,
            "stance_rule_evidence": ";".join(evidence),
            "stance_rule_fired": fired,
            "legacy_final_label": str(leg.at[pid, "sentiment"]) if pid in leg.index else "",
            "thematic_frame": frame,
            "framing_evidence": ";".join(frame_ev),
        })
    stats = {
        "n_selected": len(rows),
        "id_mismatch_vs_legacy": sorted(id_mismatch),
        "rule_traceability_matches": trace_match,
        "rule_traceability_total": len(rows),
    }
    return pd.DataFrame(rows), stats


# ----------------------------------------------------------------------------
# NEWS
# ----------------------------------------------------------------------------
def build_news() -> tuple[pd.DataFrame, dict]:
    raw = pd.read_csv(PATHS["news_raw"], encoding="utf-8-sig", dtype={"post_id": str})
    legacy = pd.read_csv(PATHS["news_legacy"], encoding="utf-8-sig", dtype={"post_id": str})
    leg = legacy.set_index(legacy["post_id"].astype(str))
    id_mismatch = set(raw["post_id"]) ^ set(leg.index)

    rows, trace_match = [], 0
    for _, r in raw.iterrows():
        pid = str(r["post_id"])
        full_text = str(r.get("full_text", ""))
        # legacy news: rule layer input = FULL text (not lead); framing = FULL text
        model_native = str(leg.at[pid, "sentiment_raw"]) if pid in leg.index else ""
        model_score = leg.at[pid, "sentiment_score"] if pid in leg.index else None
        model_label = MODEL_LABEL_MAP.get(model_native)

        trace_label, _, _ = nc.apply_stance_rule(full_text, model_native, "news")
        if trace_label == str(leg.at[pid, "sentiment"]):
            trace_match += 1

        rule_label, evidence, fired = nc.apply_stance_rule(full_text, model_native, "news")
        frame, _, frame_ev = nc.classify_framing(full_text)
        lang = nc.detect_language(full_text)

        rows.append({
            "platform": "Media Berita Online",
            "post_id": pid,
            "created_at": r.get("created_at", ""),
            "created_at_note": "legacy scraper stamped scrape-day date on RSS "
                               "date-parse failure (AUD-08); treat 2026-09-04 "
                               "rows with caution",
            "username": r.get("username", ""),
            "user_location": r.get("user_location", ""),
            "media_source": r.get("media_source", ""),
            "url": r.get("url", ""),
            "language": lang,
            "language_source": "langdetect_seed0",
            "origin_country": "",
            "origin_bloc": "",
            "bloc_basis": "outlet_country",
            "topic_country_mentions": "",
            "country_bloc": r.get("country_bloc", ""),
            "full_text": full_text,
            "clean_text": "",
            "clean_text_matches_legacy": "",
            "sentiment_model": model_label,
            "sentiment_model_score": float(model_score) if pd.notna(model_score) else None,
            "inference_source": "legacy_raw_recovered",
            "stance_target": nc.STANCE_TARGET,
            "stance_rule_variant": "news",
            "stance_rule_adjusted": rule_label,
            "stance_rule_evidence": ";".join(evidence),
            "stance_rule_fired": fired,
            "legacy_final_label": str(leg.at[pid, "sentiment"]) if pid in leg.index else "",
            "thematic_frame": frame,
            "framing_evidence": ";".join(frame_ev),
        })
    stats = {
        "n_selected": len(rows),
        "id_mismatch_vs_legacy": sorted(id_mismatch),
        "rule_traceability_matches": trace_match,
        "rule_traceability_total": len(rows),
    }
    return pd.DataFrame(rows), stats


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------
def main() -> None:
    manifest: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "langdetect_available": nc._LANGDETECT_AVAILABLE,
        "transformers_available": False,
        "purpose": "Repaired master dataset (pilot corpus). NO human gold-standard "
                   "validation exists; no kappa/precision/recall/F1 may be reported.",
        "provenance_findings": {
            "x_annotations_not_reproducible_from_shipped_code":
                "The legacy master's X rows use the NEWS label vocabulary "
                "('Negatif (Kritis terhadap Posisi/Diplomasi RI)', lowercase "
                "English raw labels) and do not satisfy the v2 X pipeline's "
                "rule/passthrough relationship for 237/237 no-fire rows. They "
                "were produced by an unshipped pipeline. The repaired dataset "
                "therefore recovers raw model labels deterministically from "
                "7_hasil4_x where the rule layer did not fire, and marks the "
                "remaining rows 'requires_rerun' rather than fabricating them.",
            "youtube_emoji_only_rows":
                "2 YouTube comments clean to an empty string (emoji/URL-only); "
                "legacy stored NaN for them. Kept with empty clean_text.",
        },
        "input_sha256": {k: sha256(v) for k, v in PATHS.items()},
    }

    log("Building Platform X ...")
    x_df, x_stats = build_x()
    log("Building YouTube ...")
    yt_df, yt_stats = build_yt()
    log("Building News ...")
    news_df, news_stats = build_news()

    master = pd.concat([x_df, yt_df, news_df], ignore_index=True)

    # integrity assertions on the repaired artifact
    assert len(master) == len(x_df) + len(yt_df) + len(news_stats and news_df), "row count"
    assert master["post_id"].duplicated().sum() == 0, "duplicate post_id in repaired master"
    assert set(master["platform"].unique()) == {
        "Platform X (Twitter)", "YouTube Comments", "Media Berita Online"}

    # label-change accounting vs legacy master
    legacy = pd.read_csv(PATHS["legacy_master"], encoding="utf-8-sig", dtype={"post_id": str})
    legacy_idx = legacy.set_index(legacy["post_id"].astype(str))
    frame_changed = bloc_changed = 0
    for _, r in master.iterrows():
        pid = str(r["post_id"])
        if pid not in legacy_idx.index:
            continue
        if str(legacy_idx.at[pid, "dominant_narrative"]) != str(r["thematic_frame"]):
            frame_changed += 1
        if str(legacy_idx.at[pid, "country_bloc"]) != str(r["country_bloc"]):
            bloc_changed += 1

    manifest["stats"] = {
        "total_rows": len(master),
        "x": x_stats,
        "youtube": yt_stats,
        "news": news_stats,
        "clean_text_matches_legacy": {
            "x": int(x_df["clean_text_matches_legacy"].sum()),
            "youtube": int(yt_df["clean_text_matches_legacy"].sum()),
        },
        "vs_legacy_master": {
            "thematic_frame_changed": frame_changed,
            "country_bloc_changed": bloc_changed,
            "note": "changes are EXPECTED: residual frames moved to "
                    "'Other/No-Frame'; X blocs now derive from profile "
                    "location with word-boundary matching (AUD-04/AUD-06)",
        },
        "language_distribution": master["language"].value_counts().to_dict(),
        "origin_bloc_distribution_x": x_df["origin_bloc"].value_counts().to_dict(),
        "thematic_frame_distribution": master["thematic_frame"].value_counts().to_dict(),
        "sentiment_model_distribution": master["sentiment_model"].value_counts(dropna=False).to_dict(),
        "stance_rule_fired_distribution": {
            "x": int(x_df["stance_rule_fired"].sum()),
            "youtube": int(yt_df["stance_rule_fired"].sum()),
            "news": int(news_df["stance_rule_fired"].sum()),
        },
    }

    out_csv = os.path.join(OUT_DIR, "master_triangulation_repaired.csv")
    master.to_csv(out_csv, index=False, encoding="utf-8-sig")
    with open(os.path.join(OUT_DIR, "build_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, default=str)

    log(f"Wrote {out_csv} ({len(master)} rows)")
    log(json.dumps(manifest["stats"], indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
