"""pipeline/sentiment.py — sentiment inference stage (English-only).

Preserves the current behavior exactly:
  - model identity from configs/models.yaml (cardiffnlp/twitter-roberta-base-sentiment-latest),
  - model-card preprocessing (mentions -> '@user', links -> 'http'),
  - label order per the official model card (0=negative, 1=neutral, 2=positive),
  - English-only language guard,
  - LOUD failure (no silent fallback, no default labels),
  - per-text inference loop (batching is M3 scope, explicitly excluded here).

No new inference is run against the historical dataset in M2. Historical
predictions in the master dataset remain historical (inference_source is
never relabeled).
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from config_loader import load_models_config  # noqa: E402
import nlp_core as _core  # noqa: E402

_MODELS = load_models_config()["sentiment"]
MODEL_NAME = _MODELS["model_name"]
LABELS: List[str] = _MODELS["label_order"]
LANGUAGE_GUARD = _MODELS.get("language_guard", "english_only")
from config_loader import load_pipeline_config  # noqa: E402
PIPELINE_VERSION = load_pipeline_config()["pipeline_version"]


class SentimentError(Exception):
    """Raised when the sentiment model cannot be loaded or run. Loud, never silent."""


def resolved_model_version(model) -> str:
    """T3: the ACTUAL model revision resolved at load time (Hugging Face sets
    `_commit_hash` on the config when loading from the Hub). Returns the
    configured registry value, or 'unknown' when it cannot be determined —
    never an invented version."""
    resolved = getattr(getattr(model, "config", None), "_commit_hash", None)
    if resolved:
        return str(resolved)
    registry = _MODELS.get("revision", "unknown")
    return registry if isinstance(registry, str) else "unknown"


def model_card_preprocess(text: str) -> str:
    """Preprocessing expected by the model card (delegates to nlp_core)."""
    return _core.clean_for_model_card(text)


def english_only_mask(languages: List[str]) -> List[bool]:
    """True where the row is eligible for the English-only model.

    The guard is strict: only the exact API/detected value 'en' passes; 'und',
    'id', and every other value is skipped (never guessed, never defaulted).
    """
    return [lang == "en" for lang in languages]


def load_model() -> Tuple[object, object, str]:
    """Load the configured model. Raises SentimentError loudly on any failure.
    There is NO fallback inference and NO default-label path."""
    try:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
    except Exception as e:
        raise SentimentError(
            f"torch/transformers unavailable ({e}). Run this in Google Colab. "
            "NO fallback inference is permitted.") from e
    try:
        tok = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        print(f"[inference] model loaded on {device}: {MODEL_NAME}")
        return tok, model, device
    except Exception as e:
        raise SentimentError(
            f"cannot load {MODEL_NAME}: {e}. Check network/HF access. "
            "NO fallback inference is permitted.") from e


def predict(texts: List[str], tok, model, device: str) -> List[Tuple[str, float]]:
    """Per-text inference (M2 semantics, identical to the pre-split loop).
    Batching is M3 scope and is intentionally NOT implemented here."""
    import torch
    out: List[Tuple[str, float]] = []
    with torch.no_grad():
        for i, t in enumerate(texts):
            enc = tok(t, return_tensors="pt", truncation=True, max_length=512).to(device)
            logits = model(**enc).logits[0]
            probs = torch.softmax(logits, dim=-1)
            idx = int(probs.argmax().item())
            out.append((LABELS[idx], round(float(probs[idx].item()), 4)))
            if (i + 1) % 100 == 0:
                print(f"[inference] {i + 1}/{len(texts)}")
    return out
