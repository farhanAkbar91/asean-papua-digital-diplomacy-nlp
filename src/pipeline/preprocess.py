"""pipeline/preprocess.py — preprocessing stage functions.

Thin, behavior-preserving delegation to the audited implementations in
src/nlp_core.py. No regex or cleaning semantics are modified here.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import nlp_core as _core  # noqa: E402


def clean_for_lexicon(text: str) -> str:
    """Light cleaning for lexicon/rule layers (legacy-equivalent)."""
    return _core.clean_for_lexicon(text)


def clean_for_model_card(text: str) -> str:
    """Model-card preprocessing: mentions -> '@user', links -> 'http'."""
    return _core.clean_for_model_card(text)


def clean_news_text(text: str) -> str:
    """News body cleaning (wire header strip, character filter)."""
    return _core.clean_news_text(text)


def extract_lead_text(full_text: str, max_words: int | None = None) -> str:
    """Headline + first N words (default from configs/pipeline.yaml)."""
    return _core.extract_lead_text(full_text, max_words=max_words)


def lead_max_words() -> int:
    """Configured lead length (configs/pipeline.yaml)."""
    return _core._PIPELINE_CFG["lead_max_words"]
