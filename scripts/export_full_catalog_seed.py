from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

DEFAULT_DATABASE = Path("instance/manga.sqlite")
DEFAULT_OUTPUT = Path("app/db/full_catalog.sql")
ARTICLE_COLUMNS = (
    "name",
    "genres",
    "universe",
    "image",
    "price",
    "stock",
    "release_day",
    "created_at",
)


def _quote_sql(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, int | float):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def export_full_catalog(database: Path, output: Path) -> int:
    if not database.exists():
        raise FileNotFoundError(f"Database not found: {database}")

    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute(
            f"""
            SELECT {", ".join(ARTICLE_COLUMNS)}
            FROM articles
            ORDER BY id
            """
        ).fetchall()
    finally:
        connection.close()

    if not rows:
        raise RuntimeError("No articles found to export.")

    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "PRAGMA foreign_keys = ON;",
        "",
        "DELETE FROM orders_articles;",
        "DELETE FROM cart_items;",
        "DELETE FROM favorites;",
        "DELETE FROM history;",
        "DELETE FROM detail_articles_public;",
        "DELETE FROM articles;",
        "DELETE FROM sqlite_sequence WHERE name = 'articles';",
        "",
        f"INSERT INTO articles ({', '.join(ARTICLE_COLUMNS)}) VALUES",
    ]

    values = []
    for row in rows:
        values.append(
            "    (" + ", ".join(_quote_sql(row[column]) for column in ARTICLE_COLUMNS) + ")"
        )

    lines.append(",\n".join(values) + ";")
    lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export the real local catalog to app/db/full_catalog.sql."
    )
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    total = export_full_catalog(args.database, args.output)
    print(f"Exported {total} articles to {args.output}")


if __name__ == "__main__":
    main()
