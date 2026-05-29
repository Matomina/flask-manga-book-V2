from __future__ import annotations

import ast
import re
from pathlib import Path

LEGACY_SCHEMA = Path("../flask-manga-book/manga/schema.sql")
OUTPUT = Path("app/db/legacy_articles_seed.sql")

ALLOWED_GENRES = {"manga", "figurine", "textile", "vaisselle", "goodies"}
ALLOWED_UNIVERSES = {
    None,
    "naruto",
    "jujutsu_kaisen",
    "one_piece",
    "demon_slayer",
    "dragon_ball",
}
ALLOWED_RELEASE_DAYS = {
    None,
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Sans jour fixe",
}


def find_articles_insert(sql: str) -> str:
    match = re.search(
        r"INSERT INTO articles\s*\(name,\s*genres,\s*universe,\s*image,\s*price,\s*release_day\)\s*VALUES\s*(.*?);",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Bloc INSERT INTO articles introuvable dans le schema legacy.")
    return match.group(1)


def split_rows(values_block: str) -> list[str]:
    rows: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    index = 0

    while index < len(values_block):
        char = values_block[index]
        next_char = values_block[index + 1] if index + 1 < len(values_block) else ""

        if depth == 0 and char not in "(":
            index += 1
            continue

        current.append(char)

        if char == "'" and next_char == "'":
            current.append(next_char)
            index += 2
            continue

        if char == "'":
            in_string = not in_string
        elif not in_string:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    row = "".join(current).strip().rstrip(",")
                    if row.startswith("(") and row.endswith(")"):
                        rows.append(row)
                    current = []

        index += 1

    return rows


def sql_tuple_to_python_tuple(row: str) -> tuple[object, ...]:
    normalized = re.sub(r"\bNULL\b", "None", row, flags=re.IGNORECASE)
    normalized = normalized.replace("''", "\\'")
    parsed = ast.literal_eval(normalized)

    if not isinstance(parsed, tuple):
        raise ValueError(f"Ligne article non tuple: {row}")

    return parsed


def parse_sql_row(row: str) -> tuple[str, str, str | None, str, float, str | None]:
    parsed = sql_tuple_to_python_tuple(row)

    if len(parsed) != 6:
        raise ValueError(f"Ligne article invalide: {row}")

    name, genres, universe, image, price, release_day = parsed

    if not isinstance(name, str):
        raise ValueError(f"Nom invalide: {name}")
    if not isinstance(genres, str) or genres not in ALLOWED_GENRES:
        raise ValueError(f"Genre non autorise: {genres} pour {name}")
    if universe not in ALLOWED_UNIVERSES:
        raise ValueError(f"Univers non autorise: {universe} pour {name}")
    if not isinstance(image, str) or not image.startswith("image/"):
        raise ValueError(f"Image invalide: {image} pour {name}")
    if release_day not in ALLOWED_RELEASE_DAYS:
        raise ValueError(f"Jour de sortie non autorise: {release_day} pour {name}")

    return name, genres, universe, image, float(price), release_day


def sql_string(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def main() -> None:
    if not LEGACY_SCHEMA.exists():
        raise FileNotFoundError(
            f"Schema legacy introuvable: {LEGACY_SCHEMA}. "
            "Verifie que les deux repos sont cote a cote."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    sql = LEGACY_SCHEMA.read_text(encoding="utf-8")
    values_block = find_articles_insert(sql)
    rows = split_rows(values_block)

    if not rows:
        raise RuntimeError("Aucune ligne article detectee dans le bloc INSERT legacy.")

    parsed_rows = [parse_sql_row(row) for row in rows]

    seen_names: set[str] = set()
    unique_rows = []
    duplicates = []

    for row in parsed_rows:
        name = row[0]
        if name in seen_names:
            duplicates.append(name)
            continue
        seen_names.add(name)
        unique_rows.append(row)

    lines = [
        "PRAGMA foreign_keys = ON;",
        "",
        "-- Seed catalogue public migre depuis V1.",
        "-- Donnees exclues volontairement : users, favoris, historique, commandes, contact, forum.",
        "",
        "DELETE FROM detail_articles_public;",
        "DELETE FROM articles;",
        "",
        "INSERT INTO articles (name, genres, universe, image, price, release_day) VALUES",
    ]

    article_values = []
    for name, genres, universe, image, price, release_day in unique_rows:
        article_values.append(
            "("
            f"{sql_string(name)}, "
            f"{sql_string(genres)}, "
            f"{sql_string(universe)}, "
            f"{sql_string(image)}, "
            f"{price:.2f}, "
            f"{sql_string(release_day)}"
            ")"
        )

    lines.append(",\n".join(article_values) + ";")
    lines.append("")
    lines.append("-- Descriptions generiques propres, sans donnees personnelles.")
    lines.append(
        "INSERT INTO detail_articles_public (article_id, description)\n"
        "SELECT id, 'Decouvrez ' || name || "
        "' dans le catalogue MangaBook. Un article selectionne pour les passionnes de mangas, figurines et goodies.' "
        "FROM articles;"
    )
    lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Articles legacy lus      : {len(parsed_rows)}")
    print(f"Articles uniques generes : {len(unique_rows)}")
    print(f"Doublons ignores         : {len(duplicates)}")
    print(f"Fichier genere           : {OUTPUT}")


if __name__ == "__main__":
    main()
