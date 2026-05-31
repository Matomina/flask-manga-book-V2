from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_db

ARTICLE_COLUMNS = """
a.id,
a.name,
a.genres,
a.universe,
a.image,
a.price,
a.stock,
a.release_day,
a.created_at
"""

ARTICLE_SELECT = f"""
SELECT {ARTICLE_COLUMNS}
FROM articles AS a
"""

RELEASE_DAY_ORDER = [
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
    "Sans jour fixe",
]

GOODIES_UNIVERSES = [
    ("naruto", "Naruto"),
    ("jujutsu_kaisen", "Jujutsu Kaisen"),
    ("one_piece", "One Piece"),
    ("demon_slayer", "Demon Slayer"),
    ("dragon_ball", "Dragon Ball"),
]

GOODIES_CATEGORIES = [
    ("figurine", "Figurines"),
    ("textile", "Textile"),
    ("vaisselle", "Vaisselle"),
]

CATALOG_SORT_COLUMNS = {
    "date": "a.created_at",
    "name": "a.name",
    "price": "a.price",
}

CATALOG_SORT_ORDERS = {"asc", "desc"}


def _execute_write(query: str, params: tuple = ()) -> None:
    """Exécuter une requête d'écriture et valider la transaction."""
    db = get_db()
    db.execute(query, params)
    db.commit()


def _normalize_text(value: str | None) -> str:
    """Nettoyer une chaîne utilisateur."""
    return (value or "").strip()


def _catalog_order_by(sort: str | None = None, order: str | None = None) -> str:
    """Construire un ORDER BY catalogue depuis une allowlist stricte."""
    normalized_sort = _normalize_text(sort).lower() or "date"
    normalized_order = _normalize_text(order).lower() or "desc"

    sort_column = CATALOG_SORT_COLUMNS.get(normalized_sort, "a.created_at")
    sort_order = normalized_order if normalized_order in CATALOG_SORT_ORDERS else "desc"

    return f"ORDER BY {sort_column} {sort_order.upper()}, a.id DESC"


def _article_exists(article_id: int) -> bool:
    """Vérifier si un article existe."""
    db = get_db()
    row = db.execute(
        """
        SELECT 1
        FROM articles
        WHERE id = ?
        """,
        (article_id,),
    ).fetchone()
    return row is not None


def get_all_articles() -> list[sqlite3.Row]:
    """Récupérer tous les articles triés par date de création décroissante."""
    db = get_db()
    return db.execute(
        f"""
        {ARTICLE_SELECT}
        ORDER BY a.created_at DESC, a.id DESC
        """
    ).fetchall()


def search_articles(
    query: str | None = None,
    genre: str | None = None,
    universe: str | None = None,
    release_day: str | None = None,
    sort: str | None = None,
    order: str | None = None,
) -> list[sqlite3.Row]:
    """Rechercher, filtrer et trier les articles du catalogue."""
    normalized_query = _normalize_text(query).lower()
    normalized_genre = _normalize_text(genre)
    normalized_universe = _normalize_text(universe).lower()
    normalized_release_day = _normalize_text(release_day)

    where_clauses: list[str] = []
    params: list[Any] = []

    if normalized_query:
        where_clauses.append(
            """
            (
                LOWER(a.name) LIKE ?
                OR LOWER(a.genres) LIKE ?
                OR LOWER(COALESCE(a.universe, '')) LIKE ?
            )
            """
        )
        search_value = f"%{normalized_query}%"
        params.extend([search_value, search_value, search_value])

    if normalized_genre:
        where_clauses.append("a.genres = ?")
        params.append(normalized_genre)

    if normalized_universe:
        where_clauses.append("LOWER(COALESCE(a.universe, '')) LIKE ?")
        params.append(f"%{normalized_universe}%")

    if normalized_release_day:
        where_clauses.append("a.release_day = ?")
        params.append(normalized_release_day)

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    db = get_db()
    return db.execute(
        f"""
        {ARTICLE_SELECT}
        {where_sql}
        {_catalog_order_by(sort, order)}
        """,
        tuple(params),
    ).fetchall()


def get_goodies_articles() -> list[sqlite3.Row]:
    """Récupérer les articles de type goodies."""
    return search_articles(genre="goodies")


def get_goodies_sections() -> dict[str, list[dict[str, Any]]]:
    """Récupérer les goodies groupés comme dans la V1."""
    universe_sections = []
    for universe_key, universe_label in GOODIES_UNIVERSES:
        universe_sections.append(
            {
                "key": universe_key,
                "label": universe_label,
                "articles": search_articles(genre="goodies", universe=universe_key),
            }
        )

    category_sections = []
    for category_key, category_label in GOODIES_CATEGORIES:
        category_sections.append(
            {
                "key": category_key,
                "label": category_label,
                "articles": search_articles(genre=category_key),
            }
        )

    return {
        "universes": universe_sections,
        "categories": category_sections,
    }


def get_articles_grouped_by_release_day() -> dict[str, list[sqlite3.Row]]:
    """Récupérer les articles groupés par jour de sortie."""
    db = get_db()

    rows = db.execute(
        f"""
        {ARTICLE_SELECT}
        WHERE a.release_day IS NOT NULL
        ORDER BY a.release_day ASC, a.created_at DESC, a.id DESC
        """
    ).fetchall()

    grouped_articles: dict[str, list[sqlite3.Row]] = {
        day: [] for day in RELEASE_DAY_ORDER
    }

    for article in rows:
        release_day = article["release_day"] or "Sans jour fixe"

        if release_day not in grouped_articles:
            grouped_articles["Sans jour fixe"].append(article)
            continue

        grouped_articles[release_day].append(article)

    return grouped_articles


def get_featured_articles(limit: int = 8) -> list[sqlite3.Row]:
    """Récupérer une sélection d'articles à mettre en avant sur l'accueil."""
    db = get_db()
    return db.execute(
        f"""
        {ARTICLE_SELECT}
        ORDER BY a.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()


def get_article_by_id(article_id: int) -> sqlite3.Row | None:
    """Récupérer un article par son identifiant avec son détail public éventuel."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            dap.description
        FROM articles AS a
        LEFT JOIN detail_articles_public AS dap
            ON dap.article_id = a.id
        WHERE a.id = ?
        """,
        (article_id,),
    ).fetchone()


def add_favorite(user_id: int, article_id: int) -> None:
    """Ajouter un article aux favoris de l'utilisateur."""
    if not _article_exists(article_id):
        raise ValueError("Article introuvable.")

    _execute_write(
        """
        INSERT OR IGNORE INTO favorites (user_id, article_id)
        VALUES (?, ?)
        """,
        (user_id, article_id),
    )


def remove_favorite(user_id: int, article_id: int) -> None:
    """Retirer un article des favoris de l'utilisateur."""
    _execute_write(
        """
        DELETE FROM favorites
        WHERE user_id = ? AND article_id = ?
        """,
        (user_id, article_id),
    )


def get_user_favorites(user_id: int) -> list[sqlite3.Row]:
    """Récupérer les articles favoris d'un utilisateur."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            f.created_at AS favorited_at
        FROM favorites AS f
        JOIN articles AS a ON a.id = f.article_id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC, a.id DESC
        """,
        (user_id,),
    ).fetchall()


def add_to_history(user_id: int, article_id: int) -> None:
    """Ajouter un article à l'historique ou mettre à jour sa date de consultation."""
    if not _article_exists(article_id):
        raise ValueError("Article introuvable.")

    _execute_write(
        """
        INSERT INTO history (user_id, article_id)
        VALUES (?, ?)
        ON CONFLICT(user_id, article_id)
        DO UPDATE SET viewed_at = CURRENT_TIMESTAMP
        """,
        (user_id, article_id),
    )


def get_user_history(user_id: int) -> list[sqlite3.Row]:
    """Récupérer l'historique d'un utilisateur."""
    db = get_db()
    return db.execute(
        """
        SELECT
            a.id,
            a.name,
            a.genres,
            a.universe,
            a.image,
            a.price,
            a.stock,
            a.release_day,
            a.created_at,
            h.viewed_at
        FROM history AS h
        JOIN articles AS a ON a.id = h.article_id
        WHERE h.user_id = ?
        ORDER BY h.viewed_at DESC, a.id DESC
        """,
        (user_id,),
    ).fetchall()


def create_contact_message(
    user_id: int, sujet: str | None, message: str | None
) -> None:
    """Créer un message de contact."""
    normalized_sujet = _normalize_text(sujet)
    normalized_message = _normalize_text(message)

    if not normalized_sujet or not normalized_message:
        raise ValueError("Le sujet et le message sont obligatoires.")

    _execute_write(
        """
        INSERT INTO contact (user_id, sujet, message)
        VALUES (?, ?, ?)
        """,
        (user_id, normalized_sujet, normalized_message),
    )
