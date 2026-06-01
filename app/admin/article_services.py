from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_db

VALID_ARTICLE_GENRES = {"manga", "figurine", "textile", "vaisselle", "goodies"}
VALID_ARTICLE_UNIVERSES = {
    "naruto",
    "jujutsu_kaisen",
    "one_piece",
    "demon_slayer",
    "dragon_ball",
}
VALID_RELEASE_DAYS = {
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Sans jour fixe",
}


def _normalize_str(value: Any) -> str:
    return str(value or "").strip()


def _normalize_optional_str(value: Any) -> str | None:
    cleaned = _normalize_str(value)
    return cleaned or None


def get_all_articles_admin() -> list[sqlite3.Row]:
    db = get_db()
    return db.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()


def get_article_by_id_admin(article_id: int) -> sqlite3.Row | None:
    db = get_db()
    return db.execute(
        """
        SELECT id, name, genres, universe, image, price, stock, release_day, created_at
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()


def create_article(data: dict[str, Any]) -> None:
    db = get_db()
    db.execute(
        """
        INSERT INTO articles (
            name,
            genres,
            universe,
            image,
            price,
            stock,
            release_day
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["genres"],
            data["universe"],
            data["image"],
            data["price"],
            data["stock"],
            data["release_day"],
        ),
    )
    db.commit()


def update_article(article_id: int, data: dict[str, Any]) -> bool:
    db = get_db()
    cursor = db.execute(
        """
        UPDATE articles
        SET
            name = ?,
            genres = ?,
            universe = ?,
            image = ?,
            price = ?,
            stock = ?,
            release_day = ?
        WHERE id = ?
        """,
        (
            data["name"],
            data["genres"],
            data["universe"],
            data["image"],
            data["price"],
            data["stock"],
            data["release_day"],
            article_id,
        ),
    )
    db.commit()
    return cursor.rowcount > 0


def delete_article(article_id: int) -> bool:
    db = get_db()
    cursor = db.execute(
        "DELETE FROM articles WHERE id = ?",
        (article_id,),
    )
    db.commit()
    return cursor.rowcount > 0


def validate_article_data(
    data: dict[str, Any],
    *,
    require_image: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    name = _normalize_str(data.get("name"))
    genres = _normalize_str(data.get("genres"))
    universe = _normalize_optional_str(data.get("universe"))
    image = _normalize_optional_str(data.get("image"))
    release_day = _normalize_optional_str(data.get("release_day"))

    try:
        price = float(data.get("price", 0))
        if price < 0:
            errors.append("Le prix doit être positif.")
    except TypeError, ValueError:
        errors.append("Prix invalide.")
        price = 0.0

    try:
        stock = int(data.get("stock", 0))
        if stock < 0:
            errors.append("Stock invalide.")
    except TypeError, ValueError:
        errors.append("Stock invalide.")
        stock = 0

    if not name:
        errors.append("Le nom est obligatoire.")

    if genres not in VALID_ARTICLE_GENRES:
        errors.append("Genre invalide.")

    if universe is not None and universe not in VALID_ARTICLE_UNIVERSES:
        errors.append("Univers invalide.")

    if release_day is not None and release_day not in VALID_RELEASE_DAYS:
        errors.append("Jour de sortie invalide.")

    if require_image and not image:
        errors.append("Image obligatoire.")

    clean_data = {
        "name": name,
        "genres": genres,
        "universe": universe,
        "image": image,
        "price": price,
        "stock": stock,
        "release_day": release_day,
    }
    return clean_data, errors
