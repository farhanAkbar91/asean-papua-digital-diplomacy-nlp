"""pipeline/config.py — stable facade over the M1 configuration loader.

Single source of truth remains src/config_loader.py + configs/*.yaml.
This module adds no parsing, no defaults, and no second configuration source.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from config_loader import (  # noqa: E402,F401  (re-exported deliberately)
    CONFIG_DIR,
    ConfigError,
    load_framing_config,
    load_models_config,
    load_pipeline_config,
    load_rules_config,
)

__all__ = [
    "CONFIG_DIR", "ConfigError",
    "load_framing_config", "load_rules_config",
    "load_pipeline_config", "load_models_config",
]
