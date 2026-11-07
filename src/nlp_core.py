"""
nlp_core.py — Shared deterministic NLP core for the REPAIRED ASEAN-Papua pipeline.

Recovery design rules (from the 2026-11-07 forensic audit, AUD-01..AUD-18):
  R1. Transformer output is the AUTHORITATIVE label. The keyword "context-aware
      adjustment" is retained ONLY as a separately reported experimental layer;
      it never overwrites the model label.
  R2. No silent inference fallbacks. A model failure must raise, never yield
      fabricated "Neutral" labels with hard-coded 0.85 scores.
  R3. Word-boundary matching everywhere. Substring tokens such as "un", "la",
      "sg", "kl", "my", "id" caused verified misclassification (Netherlands ->
      "Laos"; "puncak" -> "Mitra Global") and are banned.
  R4. The framing residual is "Other/No-Frame". It must NEVER be relabeled into
      a coded frame (the legacy master mapped 508 zero-match residuals into
      "Diplomasi & Hubungan Internasional").
  R5. Every rule-based decision stores the keywords that triggered it
      (evidence), so all classifications remain auditable.
  R6. Language is detected/normalized before any English-only model is applied;
      the corpus composition (en + id, NOT en/ms/fr) is reported as measured.

All functions are pure and unit-testable without torch/transformers.
Legacy keyword lists are preserved verbatim (per-platform) so that the builder
can reproduce legacy behaviour for traceability verification.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# M1: externalized configuration — SINGLE ACTIVE SOURCE (configs/*.yaml).
# The pre-change in-code literals are preserved only as witnesses in
# tests/test_m1_config.py; keeping them here as well would create two
# configuration sources that could silently diverge.
from config_loader import load_framing_config, load_pipeline_config, load_rules_config

_FRAMING_CFG = load_framing_config()
_RULES_CFG = load_rules_config()
_PIPELINE_CFG = load_pipeline_config()
_LID_MIN_CHARS = _PIPELINE_CFG["lid_min_chars"]

# ============================================================================
# 1. TEXT CLEANING
# ============================================================================

# Legacy light cleaning (identical regex to the shipped pipelines) — kept so the
# builder can reproduce legacy inputs bit-for-bit for traceability checks.
def clean_for_lexicon(text: str) -> str:
    """Light clean for lexicon/rule layers (legacy-equivalent)."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^\w\s#]", " ", text)
    return " ".join(text.split())


def clean_for_model_card(text: str) -> str:
    """Preprocessing expected by cardiffnlp Twitter-RoBERTa model cards:
    replace usernames with '@user' and links with 'http' (per the official
    model card example). Used for transformer input in run_inference.py."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"https?://\S+|www\.\S+", "http", text)
    text = re.sub(r"@\w+", "@user", text)
    return " ".join(text.split())


# ============================================================================
# 2. LANGUAGE HANDLING
# ============================================================================

# X/Twitter API `lang` uses the legacy code "in" for Indonesian (BCP-47 quirk).
X_LANG_NORMALIZATION = {
    "in": "id",       # Indonesian (API legacy code)
    "en": "en",
    "zxx": "zxx",     # no linguistic content
    "und": "und",     # undetermined
}

_LANGDETECT_AVAILABLE = False
try:  # optional dependency; pipeline stays usable without it
    from langdetect import DetectorFactory, detect as _ld_detect

    DetectorFactory.seed = _PIPELINE_CFG["langdetect_seed"]  # deterministic (config)
    _LANGDETECT_AVAILABLE = True
except Exception:  # pragma: no cover - exercised only when lib missing
    pass


def normalize_x_language(code: str) -> str:
    """Normalize X API language codes; unknown codes pass through unchanged."""
    if not isinstance(code, str) or not code:
        return "und"
    return X_LANG_NORMALIZATION.get(code, code)


def detect_language(text: str) -> str:
    """Detect language via langdetect (seeded, deterministic). Returns ISO-639-1
    or 'und' on failure/empty. NOTE: langdetect is a heuristic LID; texts shorter
    shorter than the configured minimum (pipeline.yaml language_detection.min_chars) are unreliable and are returned as 'und' by convention
    (documented limitation)."""
    if not isinstance(text, str) or len(text.strip()) < _LID_MIN_CHARS:
        return "und"
    if not _LANGDETECT_AVAILABLE:
        return "und"
    try:
        return _ld_detect(text)
    except Exception:
        return "und"


# ============================================================================
# 3. GEOGRAPHIC ORIGIN & BLOC CLASSIFICATION (word-boundary gazetteer)
# ============================================================================

# Country keyword gazetteer. ALL patterns are matched with word boundaries.
# Two-letter/short codes are only matched as standalone tokens. This replaces
# the legacy substring matching whose collisions are documented in the audit.
COUNTRY_KEYWORDS: Dict[str, List[str]] = {
    "Indonesia": ["indonesia", "indonesian", "jakarta", "surabaya", "bandung",
                  "yogyakarta", "jogja", "bali", "medan", "semarang", "makassar",
                  "palembang", "depok", "tangerang", "bekasi", "bogor", "jayapura"],
    "Malaysia": ["malaysia", "malaysian", "kuala lumpur", "penang", "johor",
                 "selangor", "cyberjaya", "putrajaya", "sabah", "sarawak",
                 "petaling jaya"],
    "Singapore": ["singapore", "singapura"],
    "Thailand": ["thailand", "bangkok", "chiang mai", "phuket"],
    "Philippines": ["philippines", "manila", "quezon city", "cebu", "davao"],
    "Vietnam": ["vietnam", "hanoi", "ho chi minh", "saigon"],
    "Myanmar": ["myanmar", "yangon", "mandalay", "burma"],
    "Cambodia": ["cambodia", "phnom penh"],
    "Laos": ["laos", "vientiane"],
    "Brunei": ["brunei", "bandar seri begawan"],
    "Papua New Guinea": ["papua new guinea", "png", "port moresby"],
    "Vanuatu": ["vanuatu", "port vila"],
    "Fiji": ["fiji", "suva"],
    "Solomon Islands": ["solomon islands", "solomon", "honiara"],
    "New Caledonia": ["new caledonia", "noumea", "kanaky"],
    "Australia": ["australia", "sydney", "melbourne", "canberra"],
    "New Zealand": ["new zealand", "auckland", "wellington"],
    "United Kingdom": ["united kingdom", "england", "scotland", "london"],
    "United States": ["united states", "usa", "washington"],
    "Netherlands": ["netherlands", "nederland", "den haag", "amsterdam"],
    "Switzerland": ["switzerland", "geneva"],
    "Qatar": ["qatar", "doha"],
}

BLOC_BY_COUNTRY: Dict[str, str] = {}
for _c in ["Malaysia", "Singapore", "Thailand", "Philippines", "Vietnam",
           "Myanmar", "Cambodia", "Laos", "Brunei"]:
    BLOC_BY_COUNTRY[_c] = "Blok ASEAN"
for _c in ["Papua New Guinea", "Vanuatu", "Fiji", "Solomon Islands",
           "New Caledonia"]:
    BLOC_BY_COUNTRY[_c] = "Blok Pasifik & Melanesia"
for _c in ["Australia", "New Zealand", "United Kingdom", "United States",
           "Netherlands", "Switzerland", "Qatar"]:
    BLOC_BY_COUNTRY[_c] = "Mitra Global"
BLOC_BY_COUNTRY["Indonesia"] = "Indonesia (Excluded)"

BLOC_UNKNOWN = "Wacana Regional Non-Spesifik"

# Compiled word-boundary patterns (built once).
_COUNTRY_PATTERNS: Dict[str, List[re.Pattern]] = {
    country: [re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
              for kw in kws]
    for country, kws in COUNTRY_KEYWORDS.items()
}


def match_country(text: str) -> Optional[str]:
    """Return the country whose keyword matches `text` (word-boundary), or None.
    Deterministic tie-break: longest matched keyword wins; then dict order."""
    if not isinstance(text, str) or not text.strip():
        return None
    best_country, best_len = None, 0
    for country, patterns in _COUNTRY_PATTERNS.items():
        for pat, kw in zip(patterns, COUNTRY_KEYWORDS[country]):
            if pat.search(text):
                if len(kw) > best_len:
                    best_country, best_len = country, len(kw)
    return best_country


def origin_from_location(user_location: str) -> Tuple[Optional[str], str]:
    """(country, bloc) derived from the profile location string ONLY.
    Unknown/empty -> (None, BLOC_UNKNOWN). Actor origin is NEVER inferred
    from tweet text (audit AUD-06: origin/topic conflation)."""
    country = match_country(user_location or "")
    if country is None:
        return None, BLOC_UNKNOWN
    return country, BLOC_BY_COUNTRY[country]


def is_indonesia_origin(user_location: str) -> bool:
    return origin_from_location(user_location)[0] == "Indonesia"


def topic_country_mentions(text: str) -> List[str]:
    """Countries explicitly mentioned in tweet/article text. Reported as a
    separate variable; never used to infer the author's origin."""
    if not isinstance(text, str):
        return []
    found = []
    for country, patterns in _COUNTRY_PATTERNS.items():
        for pat in patterns:
            if pat.search(text):
                found.append(country)
                break
    return found


# ============================================================================
# 4. FRAMING CLASSIFICATION (unified 5-frame lexicon + explicit residual)
# ============================================================================

# Unified, word-boundary lexicon — taken verbatim from the news pipeline
# (the most complete shipped variant, incl. the coded F5 "Diplomasi" frame)
# and now applied to ALL platforms. The residual is a separate category.
NARRATIVE_CATEGORIES: Dict[str, List[str]] = {
    cat: list(_FRAMING_CFG["categories"][cat])  # document order = evaluation/tie-break priority
    for cat in _FRAMING_CFG["category_priority"]
}

FRAME_RESIDUAL: str = _FRAMING_CFG["residual_label"]

_FRAME_PATTERNS: Dict[str, List[re.Pattern]] = {
    cat: [re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
          for kw in kws]
    for cat, kws in NARRATIVE_CATEGORIES.items()
}


def classify_framing(text: str) -> Tuple[str, Dict[str, int], List[str]]:
    """Word-boundary framing classification.
    Returns (dominant_frame, per-category scores, matched keywords [evidence]).
    Zero matches -> (FRAME_RESIDUAL, scores, []). KNOWN LIMITATION (documented):
    no negation handling, e.g. "no evidence of genocide" still matches F1."""
    if not isinstance(text, str):
        text = ""
    scores: Dict[str, int] = {}
    evidence: List[str] = []
    for cat, patterns in _FRAME_PATTERNS.items():
        score = 0
        for pat, kw in zip(patterns, NARRATIVE_CATEGORIES[cat]):
            if pat.search(text):
                score += 1
                evidence.append(kw)
        scores[cat] = score
    best = max(scores, key=lambda c: scores[c])  # dict order = legacy tie-break
    if scores[best] == 0:
        return FRAME_RESIDUAL, scores, []
    return best, scores, evidence


# ============================================================================
# 5. KEYWORD RULE LAYER ("context-aware adjustment") — EXPERIMENTAL, SEPARATE
# ============================================================================
# Legacy keyword lists are preserved VERBATIM per platform so the builder can
# reproduce legacy behaviour exactly for traceability verification.
# The repaired pipeline stores this layer in a SEPARATE column and never
# overwrites `sentiment_model`.

STANCE_RULES: Dict[str, Dict] = _RULES_CFG["variants"]

STANCE_TARGET = _RULES_CFG["stance_target"]


def apply_stance_rule(text: str, base_label: str,
                      variant: str) -> Tuple[str, List[str], bool]:
    """EXPERIMENTAL keyword calibration layer (legacy-equivalent logic).
    Returns (adjusted_label, matched_keywords, fired).
    KNOWN DIRECTIONAL ASSUMPTION (documented, must be validated by humans):
    ANY mention of e.g. "referendum"/"independence"/"human rights" flips the
    label to Critical — even in pro-government sentences such as
    "Indonesia rejects the referendum push". This is why the layer is
    experimental and must never replace the model label in headline results.
    """
    cfg = STANCE_RULES[variant]
    text_lower = (text or "").lower()
    crit_hits = [kw for kw in cfg["critical"] if kw in text_lower]
    supp_hits = [kw for kw in cfg["supportive"] if kw in text_lower]
    crit_score, supp_score = len(crit_hits), len(supp_hits)

    if crit_score > 0 and crit_score >= supp_score:
        label = ("Negatif (Kritis terhadap Posisi/Diplomasi RI)" if variant == "news"
                 else "Negatif (Kritis terhadap Diplomasi RI)" if variant == "youtube"
                 else "Negatif (Kritis)")
    elif supp_score > 0 and supp_score > crit_score:
        label = ("Positif (Mendukung Pembangunan/Kedaulatan RI)" if variant == "news"
                 else "Positif (Mendukung Pembangunan/NKRI)" if variant == "youtube"
                 else "Positif (Mendukung)")
    else:
        label = cfg["passthrough"].get(base_label, base_label)
    return label, crit_hits + supp_hits, bool(crit_hits or supp_hits)


def recover_x_base_label(legacy_clean_text: str,
                         legacy_adjusted_label: str) -> Optional[str]:
    """Recover the raw model label for legacy X rows where the rule layer did
    NOT fire (then adjusted == passthrough(base)). Returns None when the rule
    layer fired (raw model label is unrecoverable without re-inference)."""
    _, _, fired = apply_stance_rule(legacy_clean_text, "", variant="x_v2")
    if fired:
        return None
    inverse = {"Positif (Mendukung)": "Positif",
               "Negatif (Kritis)": "Negatif",
               "Netral": "Netral"}
    return inverse.get(legacy_adjusted_label)


# ============================================================================
# 6. NEWS LEAD EXTRACTION (inverted pyramid)
# ============================================================================

def clean_news_text(text: str) -> str:
    """Legacy news cleaning (wire header strip, char filter) — kept identical
    for traceability; used before lead extraction."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"^[A-Z\s]{2,15}:\s*", "", text)
    text = re.sub(r"[^\w\s.,!?-]", " ", text)
    return " ".join(text.split())


def extract_lead_text(full_text: str, max_words: int | None = None) -> str:
    """Headline + first `max_words` words of the cleaned article body.
    Default comes from configs/pipeline.yaml (preprocessing.lead_max_words)."""
    if max_words is None:
        max_words = _PIPELINE_CFG["lead_max_words"]
    cleaned = clean_news_text(full_text)
    return " ".join(cleaned.split()[:max_words])


# ============================================================================
# 7. X SELECTION FILTERS (verbatim reproduction of the legacy 427 -> 375 step)
# ============================================================================

SPAM_USERNAMES = ["FREEPHONEFREES1", "SPAM_BOT"]
SPAM_PHRASES = [
    "conf & appd", "hubby elon", "optad", "harriet tubman", "dow conf",
    "extradition to us", "lucy", "pres trump", "fbi dir", "doj ag",
    "putin's brothel",
]
X_RELEVANCE_KEYWORDS = [
    "papua", "melanesia", "msg", "sovereignty", "human rights",
    "pacific", "ulmwp", "otsus", "indonesia", "vanuatu", "solomon", "fiji",
]
# Legacy exclusion list (substring-based) reproduced verbatim for traceability;
# the repaired origin classifier supersedes it for bloc assignment.
LEGACY_EXCLUDE_LOCATION_KEYWORDS = [
    "indonesia", "jakarta", "surabaya", "bandung", "yogyakarta", "jogja",
    "bali", "medan", "semarang", "makassar", "palembang", "depok", "tangerang",
    "bekasi", "bogor", "jayapura", "idn",
]


def is_spam(username: str, text: str) -> bool:
    if str(username).upper() in SPAM_USERNAMES:
        return True
    tl = str(text).lower()
    return any(phrase in tl for phrase in SPAM_PHRASES)


def legacy_is_indonesia_location(user_location: str) -> bool:
    if not isinstance(user_location, str) or not user_location:
        return False
    loc = user_location.lower().strip()
    return any(k in loc for k in LEGACY_EXCLUDE_LOCATION_KEYWORDS)


def is_relevant_x(text: str) -> bool:
    pat = "|".join(X_RELEVANCE_KEYWORDS)
    return bool(re.search(pat, str(text), re.IGNORECASE))
