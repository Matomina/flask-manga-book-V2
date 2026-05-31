from __future__ import annotations

from typing import Any

from app.db import get_db


class CartError(ValueError):
    pass


def _quantity(value: Any) -> int:
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise CartError("Quantité invalide.") from exc

    if quantity <= 0:
        raise CartError("Quantité invalide.")

    return quantity


def get_cart_items(user_id: int):
    db = get_db()
    return db.execute(
        """
        SELECT ci.article_id, ci.quantity, a.name, a.price, a.stock, a.image
        FROM cart_items AS ci
        JOIN articles AS a ON a.id = ci.article_id
        WHERE ci.user_id = ?
        ORDER BY ci.updated_at DESC, ci.id DESC
        """,
        (user_id,),
    ).fetchall()


def get_cart_total(user_id: int) -> float:
    items = get_cart_items(user_id)
    total = sum(item["price"] * item["quantity"] for item in items)
    return round(float(total), 2)


def add_cart_item(user_id: int, article_id: int, quantity: Any = 1) -> None:
    quantity_value = _quantity(quantity)
    db = get_db()
    article = db.execute(
        "SELECT stock FROM articles WHERE id = ?",
        (article_id,),
    ).fetchone()

    if article is None:
        raise CartError("Article introuvable.")

    current = db.execute(
        """
        SELECT quantity
        FROM cart_items
        WHERE user_id = ? AND article_id = ?
        """,
        (user_id, article_id),
    ).fetchone()

    new_quantity = quantity_value + (current["quantity"] if current else 0)
    if article["stock"] < new_quantity:
        raise CartError("Stock insuffisant.")

    db.execute(
        """
        INSERT INTO cart_items (user_id, article_id, quantity)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, article_id)
        DO UPDATE SET quantity = excluded.quantity, updated_at = CURRENT_TIMESTAMP
        """,
        (user_id, article_id, new_quantity),
    )
    db.commit()


def update_cart_item(user_id: int, article_id: int, quantity: Any) -> None:
    quantity_value = _quantity(quantity)
    db = get_db()
    article = db.execute(
        "SELECT stock FROM articles WHERE id = ?",
        (article_id,),
    ).fetchone()

    if article is None:
        raise CartError("Article introuvable.")

    if article["stock"] < quantity_value:
        raise CartError("Stock insuffisant.")

    cursor = db.execute(
        """
        UPDATE cart_items
        SET quantity = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ? AND article_id = ?
        """,
        (quantity_value, user_id, article_id),
    )
    db.commit()

    if cursor.rowcount == 0:
        raise CartError("Article absent du panier.")


def remove_cart_item(user_id: int, article_id: int) -> None:
    db = get_db()
    db.execute(
        "DELETE FROM cart_items WHERE user_id = ? AND article_id = ?",
        (user_id, article_id),
    )
    db.commit()
