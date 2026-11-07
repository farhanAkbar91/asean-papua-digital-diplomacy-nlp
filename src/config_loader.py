"""config_loader.py — M1 configuration loader (strict, deterministic, no fallbacks).

Loads the externalized YAML configuration (configs/) and validates structure and
types. Design rules (M1):
  - Deterministic: yaml.safe_load preserves document order; no sorting, no defaults.
  - Loud: missing files, missing keys, wrong types, or empty structures raise
    ConfigError. Invalid configuration NEVER yields default labels.
  - Single source of truth: after M1 the active code reads configuration ONLY
    from these files (the pre-change in-code literals are retained solely as
    test witnesses in tests/test_m1_config.py).
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"


class ConfigError(Exception):
    """Raised for missing, malformed, or invalid configuration."""


def _load_yaml(filename: str) -> Dict[str, Any]:
    path = CONFIG_DIR / filename
    if not os.path.isfile(path):
        raise ConfigError(f"missing configuration file: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"invalid YAML in {path}: {e}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"configuration root must be a mapping: {path}")
    return data


def _require_str_list(container: Dict[str, Any], key: str, ctx: str) -> List[str]:
    value = container.get(key)
    if not isinstance(value, list) or not value:
        raise ConfigError(f"{ctx}: '{key}' must be a non-empty list")
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"{ctx}: '{key}[{i}]' must be a non-empty string")
    return value


def _require_str_dict(container: Dict[str, Any], key: str, ctx: str) -> Dict[str, str]:
    value = container.get(key)
    if not isinstance(value, dict) or not value:
        raise ConfigError(f"{ctx}: '{key}' must be a non-empty mapping")
    for k, v in value.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise ConfigError(f"{ctx}: '{key}' keys and values must be strings")
    return value


def load_framing_config(path: os.PathLike | str | None = None) -> Dict[str, Any]:
    """Validate and return the framing (lexicon) configuration."""
    data = _load_yaml(path or "lexicon.yaml")
    residual = data.get("residual_label")
    if not isinstance(residual, str) or not residual.strip():
        raise ConfigError("lexicon.yaml: 'residual_label' must be a non-empty string")
    priority = _require_str_list(data, "category_priority", "lexicon.yaml")
    categories = data.get("categories")
    if not isinstance(categories, dict) or not categories:
        raise ConfigError("lexicon.yaml: 'categories' must be a non-empty mapping")
    for cat, keywords in categories.items():
        if not isinstance(cat, str) or not isinstance(keywords, list) or not keywords:
            raise ConfigError(f"lexicon.yaml: category '{cat}' must map to a non-empty list")
        for i, kw in enumerate(keywords):
            if not isinstance(kw, str) or not kw.strip():
                raise ConfigError(f"lexicon.yaml: category '{cat}' keyword [{i}] must be a non-empty string")
    if priority != list(categories.keys()):
        raise ConfigError(
            "lexicon.yaml: 'category_priority' must exactly match the 'categories' key order "
            "(evaluation/tie-break order is significant)")
    return {"residual_label": residual, "category_priority": priority, "categories": categories}


def load_rules_config(path: os.PathLike | str | None = None) -> Dict[str, Any]:
    """Validate and return the stance rule-layer configuration."""
    data = _load_yaml(path or "rules.yaml")
    target = data.get("stance_target")
    if not isinstance(target, str) or not target.strip():
        raise ConfigError("rules.yaml: 'stance_target' must be a non-empty string")
    variants = data.get("variants")
    if not isinstance(variants, dict) or not variants:
        raise ConfigError("rules.yaml: 'variants' must be a non-empty mapping")
    for name, cfg in variants.items():
        ctx = f"rules.yaml variant '{name}'"
        if not isinstance(cfg, dict):
            raise ConfigError(f"{ctx}: must be a mapping")
        _require_str_list(cfg, "critical", ctx)
        _require_str_list(cfg, "supportive", ctx)
        _require_str_dict(cfg, "passthrough", ctx)
    return {"stance_target": target, "variants": variants}


def load_pipeline_config(path: os.PathLike | str | None = None) -> Dict[str, Any]:
    """Validate and return the pipeline parameter configuration."""
    data = _load_yaml(path or "pipeline.yaml")
    lang = data.get("language_detection")
    if not isinstance(lang, dict):
        raise ConfigError("pipeline.yaml: 'language_detection' must be a mapping")
    seed = lang.get("langdetect_seed")
    min_chars = lang.get("min_chars")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ConfigError("pipeline.yaml: 'language_detection.langdetect_seed' must be an integer")
    if not isinstance(min_chars, int) or isinstance(min_chars, bool) or min_chars <= 0:
        raise ConfigError("pipeline.yaml: 'language_detection.min_chars' must be a positive integer")
    pre = data.get("preprocessing")
    if not isinstance(pre, dict):
        raise ConfigError("pipeline.yaml: 'preprocessing' must be a mapping")
    lead = pre.get("lead_max_words")
    if not isinstance(lead, int) or isinstance(lead, bool) or lead <= 0:
        raise ConfigError("pipeline.yaml: 'preprocessing.lead_max_words' must be a positive integer")
    version = data.get("pipeline_version")
    if not isinstance(version, str) or not version.strip():
        raise ConfigError("pipeline.yaml: 'pipeline_version' must be a non-empty string")
    return {"langdetect_seed": seed, "lid_min_chars": min_chars,
            "lead_max_words": lead, "pipeline_version": version}


def content_version(filename: str) -> str:
    """T3: deterministic configuration identifier — first 12 hex chars of the
    SHA-256 of the config file content. This is an ACTUAL identifier of the
    loaded configuration, never an invented version number."""
    path = CONFIG_DIR / filename
    if not os.path.isfile(path):
        raise ConfigError(f"missing configuration file: {path}")
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def load_models_config(path: os.PathLike | str | None = None) -> Dict[str, Any]:
    """Validate and return the model registry (metadata only; unknowns marked unknown)."""
    data = _load_yaml(path or "models.yaml")
    sent = data.get("sentiment")
    if not isinstance(sent, dict):
        raise ConfigError("models.yaml: 'sentiment' must be a mapping")
    name = sent.get("model_name")
    if not isinstance(name, str) or not name.strip():
        raise ConfigError("models.yaml: 'sentiment.model_name' must be a non-empty string")
    labels = sent.get("label_order")
    if not isinstance(labels, list) or len(labels) != 3 or not all(isinstance(x, str) for x in labels):
        raise ConfigError("models.yaml: 'sentiment.label_order' must be a list of exactly 3 strings "
                          "(index order per the official model card)")
    return {"sentiment": sent}
