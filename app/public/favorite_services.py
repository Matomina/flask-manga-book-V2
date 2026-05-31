from __future__ import annotations

from app.db import get_db


def toggle_favorite(user_id: int, article_id: int) -> str:
    """Ajouter ou retirer un favori et retourner le statut appliqué."""
    db = get_db()
    existing = db.execute(
        """
        SELECT id
        FROM favorites
        WHERE user_id = ? AND article_id = ?
        """,
        (user_id, article_id),
    ).fetchone()

    if existing is not None:
        db.execute(
            """
            DELETE FROM favorites
            WHERE user_id = ? AND article_id = ?
            """,
            (user_id, article_id),
        )
        db.commit()
        return "removed"

    db.execute(
        """
        INSERT INTO favorites (user_id, article_id)
        VALUES (?, ?)
        """,
        (user_id, article_id),
    )
    db.commit()
    return "added"
