from __future__ import annotations

from datetime import datetime

from flask import Flask


def register_template_filters(app: Flask) -> None:
    """Enregistrer les filtres Jinja personnalisés."""

    months_fr = {
        1: "janvier",
        2: "février",
        3: "mars",
        4: "avril",
        5: "mai",
        6: "juin",
        7: "juillet",
        8: "août",
        9: "septembre",
        10: "octobre",
        11: "novembre",
        12: "décembre",
    }

    @app.template_filter("format_datetime_fr")
    def format_datetime_fr(value: str | None) -> str:
        """Formater une date SQL en français."""
        if not value:
            return ""

        try:
            dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value

        month = months_fr[dt.month]
        return f"{dt.day:02d} {month} {dt.year} à {dt.hour:02d}h{dt.minute:02d}"