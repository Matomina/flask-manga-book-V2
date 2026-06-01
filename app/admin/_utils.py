from __future__ import annotations

from typing import Any


def normalize_str(value: Any) -> str:
    """Normaliser une valeur formulaire en chaîne nettoyée."""

    return str(value or "").strip()


def normalize_optional_str(value: Any) -> str | None:
    """Normaliser une valeur formulaire optionnelle."""

    cleaned = normalize_str(value)
    return cleaned or None
