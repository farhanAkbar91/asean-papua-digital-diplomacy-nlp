"""pipeline/langid.py — language identification stage.

Preserves the current behavior exactly:
  - X API language normalization ('in' -> 'id'),
  - langdetect with seed from configs/pipeline.yaml (0),
  - the configured minimum-length threshold (40 chars -> 'und'),
  - 'und' semantics (never guessed).

A backend seam exists for future evaluation (e.g., fastText, refactor plan
section 5.2) but ONLY the current backend is implemented and active.
"""

from __future__ import annotations

import os
import sys
from typing import List

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import nlp_core as _core  # noqa: E402

ACTIVE_BACKEND = "langdetect"


def normalize_x_language(code: str) -> str:
    """X/Twitter API language normalization ('in' -> 'id'; unknown passthrough)."""
    return _core.normalize_x_language(code)


def detect_language(text: str) -> str:
    """Detect language (langdetect, seeded; texts below the configured minimum
    length return 'und')."""
    return _core.detect_language(text)


def detect_languages(texts: List[str]) -> List[str]:
    """Bulk deterministic detection (same semantics as detect_language)."""
    return [_core.detect_language(t) for t in texts]


def lid_min_chars() -> int:
    """Configured minimum length for reliable detection."""
    return _core._LID_MIN_CHARS


def langdetect_seed() -> int:
    """Configured langdetect seed (determinism guarantee)."""
    return _core._PIPELINE_CFG["langdetect_seed"]
