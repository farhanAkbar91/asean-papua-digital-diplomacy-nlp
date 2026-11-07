"""pipeline/stance.py — stance rule layer stage (EXPERIMENTAL).

Encapsulates the existing keyword rule layer verbatim (loaded through the M1
configuration). This is an EXPERIMENTAL rule-based layer, not a validated
stance model: its outputs stay in separate columns and never replace model
predictions. No new stance model, no zero-shot NLI, no fine-tuning, no new
targets or codebook changes (all reserved for the team).
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import nlp_core as _core  # noqa: E402

STANCE_TARGET = _core.STANCE_TARGET
VARIANTS: List[str] = list(_core.STANCE_RULES.keys())  # ['x_v2', 'youtube', 'news'] — legacy order
LAYER_STATUS = "experimental_rule_layer (not a validated stance model)"


def apply_stance_rule(text: str, base_label: str, variant: str) -> Tuple[str, List[str], bool]:
    """Legacy-equivalent keyword calibration layer with evidence.
    See nlp_core.apply_stance_rule for the documented directional assumption."""
    if variant not in _core.STANCE_RULES:
        raise ValueError(f"unknown stance rule variant: {variant!r} (available: {VARIANTS})")
    return _core.apply_stance_rule(text, base_label, variant)


def recover_x_base_label(legacy_clean_text: str, legacy_adjusted_label: str):
    """Recover the raw model label for legacy X rows where the rule layer did not fire."""
    return _core.recover_x_base_label(legacy_clean_text, legacy_adjusted_label)


def rule_evidence(text: str, variant: str) -> List[str]:
    """Matched keywords only (evidence without label computation)."""
    _, evidence, _ = apply_stance_rule(text, "", variant)
    return evidence
