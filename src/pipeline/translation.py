"""pipeline/translation.py — translation interface (DISABLED by design).

M2 scope: an explicit seam only. Translation is NOT executed, NOT available,
and MUST NOT be simulated. Enabling it requires a team-approved route and
quality-check protocol (see docs/METHODOLOGY_REPAIRED.md section 3 and the
M1/M2 reports): id->en via opus-mt-id-en is verified to exist; ms->en has no
opus-mt checkpoint; all routes require human spot-checks before inference.
"""

from __future__ import annotations

from typing import List

DEFAULT_BACKEND = "none"
AVAILABLE_BACKENDS = ["none"]  # no execution backend is registered in M2


def available_backends() -> List[str]:
    """Backends registered in M2. Only the disabled 'none' backend exists."""
    return list(AVAILABLE_BACKENDS)


class TranslationError(Exception):
    """Raised when translation is requested while no backend is approved."""


def is_enabled(backend: str = DEFAULT_BACKEND) -> bool:
    """Translation is disabled in M2 for every backend."""
    return False


def translate(texts: List[str], source_lang: str, target_lang: str = "en",
              backend: str = DEFAULT_BACKEND) -> List[str]:
    """Never returns translated text in M2: raises TranslationError.

    There is no network access, no model download, and no text generation
    behind this interface. Approved future backends must be registered in
    AVAILABLE_BACKENDS and implemented behind this same seam.
    """
    raise TranslationError(
        "translation is DISABLED in M2: no approved backend is implemented "
        f"(requested backend={backend!r}, {source_lang}->{target_lang}). "
        "Enable only after team approval of the route and the quality-check "
        "protocol (docs/METHODOLOGY_REPAIRED.md section 3).")


def approved_routes() -> List[str]:
    """Routes approved for execution. Empty until a team decision exists."""
    return []
