"""
run_inference.py — Transformer inference for the repaired pipeline.

MUST be executed in an environment with torch + transformers (e.g., Google
Colab). This environment intentionally performs NO silent fallback: if the
model cannot be loaded or inference fails, the script exits with an error
(audit AUD-03: the legacy pipeline converted model failures into fabricated
"Neutral" labels with hard-coded 0.85 scores — that behaviour is banned).

Model facts (verified against the official Hugging Face model card,
2026-11-07):
  cardiffnlp/twitter-roberta-base-sentiment-latest
    - RoBERTa-base pretrained on ~124M tweets (2018-2021), fine-tuned on
      TweetEval sentiment; labels 0=Negative, 1=Neutral, 2=Positive.
    - ENGLISH-ONLY ("This model is suitable for English").
    - Expected preprocessing: usernames -> '@user', links -> 'http'
      (implemented in nlp_core.clean_for_model_card).
    - Correct citation: Loureiro et al. (2022), TimeLMs, ACL 2022 Demo.
      https://aclanthology.org/2022.acl-demo.25/

Usage:
    python src/run_inference.py --platform x      # fills requires_rerun rows
    python src/run_inference.py --platform yt     # optional re-verification
    python src/run_inference.py --platform news

Output:
    data/processed/model_labels_<platform>_refresh.csv
      columns: post_id, sentiment_model, sentiment_model_score
After running --platform x, re-run build_master_repaired.py to merge the
refreshed labels (it picks up the refresh file automatically if present).
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import nlp_core as nc  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
LABEL_MAP = {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}


def die(msg: str) -> None:
    print(f"[FATAL] {msg}", file=sys.stderr)
    sys.exit(1)


def load_model():
    try:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
    except Exception as e:
        die(f"torch/transformers unavailable ({e}). Run this in Google Colab. "
            "NO fallback inference is permitted.")
    try:
        tok = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        print(f"[inference] model loaded on {device}: {MODEL_NAME}")
        return tok, model, device
    except Exception as e:
        die(f"cannot load {MODEL_NAME}: {e}. Check network/HF access. "
            "NO fallback inference is permitted.")


def predict(texts, tok, model, device):
    import torch
    out = []
    with torch.no_grad():
        for i, t in enumerate(texts):
            enc = tok(t, return_tensors="pt", truncation=True, max_length=512).to(device)
            logits = model(**enc).logits[0]
            probs = torch.softmax(logits, dim=-1)
            idx = int(probs.argmax().item())
            out.append((LABEL_MAP[idx], round(float(probs[idx].item()), 4)))
            if (i + 1) % 100 == 0:
                print(f"[inference] {i + 1}/{len(texts)}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", choices=["x", "yt", "news"], required=True)
    args = ap.parse_args()

    tok, model, device = load_model()

    if args.platform == "x":
        # Selection reproduction identical to the builder (375 rows).
        raw = pd.read_csv(os.path.join(ROOT, "data", "raw", "asean_papua_x_tweets.csv"),
                          encoding="utf-8-sig", dtype={"tweet_id": str})
        keep = []
        for _, r in raw.iterrows():
            if nc.is_spam(r.get("username", ""), r.get("full_text", "")):
                continue
            if nc.legacy_is_indonesia_location(r.get("user_location", "")):
                continue
            if not nc.is_relevant_x(r.get("full_text", "")):
                continue
            keep.append(str(r["tweet_id"]))
        sub = raw[raw["tweet_id"].astype(str).isin(keep)].copy()
        # language guard: only English rows pass to the English-only model
        lang_list = [nc.normalize_x_language(l) for l in sub["language"]]
        id_col = sub["tweet_id"].astype(str)
        src_texts = sub["full_text"]
    else:
        path = ("data/raw/youtube_papua_asean_comments.csv" if args.platform == "yt"
                else "data/raw/news_papua_asean_articles.csv")
        sub = pd.read_csv(os.path.join(ROOT, path), encoding="utf-8-sig",
                          dtype={"post_id": str})
        sub = sub.dropna(subset=["full_text"])
        sub = sub[sub["full_text"].astype(str).str.strip().str.len() >= 10]
        lang_list = [nc.detect_language(str(t)) for t in sub["full_text"]]
        id_col = sub["post_id"].astype(str)
        src_texts = sub["full_text"]

    n_non_en = sum(1 for l in lang_list if l != "en")
    print(f"[inference] NOTE: {n_non_en}/{len(sub)} rows are non-English (or too "
          f"short to detect) -> sentiment_model=NaN. The model is English-only "
          f"per its official card; translation is a separate, quality-checked step.")
    texts = [nc.clean_for_model_card(str(t)) if l == "en" else ""
             for t, l in zip(src_texts, lang_list)]

    preds = predict(texts, tok, model, device)
    out = pd.DataFrame({
        "post_id": id_col.values,
        "sentiment_model": [p[0] if l == "en" else None
                            for p, l in zip(preds, lang_list)],
        "sentiment_model_score": [p[1] if l == "en" else None
                                   for p, l in zip(preds, lang_list)],
    })
    out_path = os.path.join(ROOT, "data", "processed",
                            f"model_labels_{args.platform}_refresh.csv")
    out.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"[inference] wrote {out_path} ({len(out)} rows). "
          f"Re-run build_master_repaired.py to merge.")


if __name__ == "__main__":
    main()
