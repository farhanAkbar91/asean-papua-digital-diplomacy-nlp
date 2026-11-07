"""pipeline/framing.py — framing classification stage.

Encapsulates the existing word-boundary lexicon classification verbatim
(loaded through the M1 configuration): five coded categories in legacy
priority order, explicit 'Other/No-Frame' residual, keyword evidence.
No keyword changes, no negation handling, no multi-label, no new taxonomy.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import nlp_core as _core  # noqa: E402

FRAME_RESIDUAL: str = _core.FRAME_RESIDUAL
CATEGORIES: Dict[str, List[str]] = _core.NARRATIVE_CATEGORIES
CATEGORY_PRIORITY: List[str] = list(CATEGORIES.keys())


def classify_framing(text: str) -> Tuple[str, Dict[str, int], List[str]]:
    """Identical semantics to nlp_core.classify_framing:
    (dominant_frame, per-category scores, matched keywords as evidence).
    Zero matches -> (FRAME_RESIDUAL, scores, [])."""
    return _core.classify_framing(text)


def classify_label(text: str) -> str:
    """Label-only convenience wrapper."""
    return _core.classify_framing(text)[0]
