from __future__ import annotations

from app.core.filters import format_datetime_fr


def test_format_datetime_fr_valid_datetime():
    result = format_datetime_fr("2026-04-18 14:35:00")
    assert result == "18 avril 2026 à 14h35"


def test_format_datetime_fr_none_returns_empty_string():
    result = format_datetime_fr(None)
    assert result == ""


def test_format_datetime_fr_empty_string_returns_empty_string():
    result = format_datetime_fr("")
    assert result == ""


def test_format_datetime_fr_invalid_value_returns_original():
    value = "date-invalide"
    result = format_datetime_fr(value)
    assert result == value


def test_format_datetime_fr_invalid_format_returns_original():
    value = "2026/04/18"
    result = format_datetime_fr(value)
    assert result == value
