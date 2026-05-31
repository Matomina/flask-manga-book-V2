from __future__ import annotations

import sqlite3

from app.db import get_db

from .cart_services import CartError, get_cart_items, get_cart_total


def create_order_from_cart(user_id: int) -> int:
    db = get_db()
    items = get_cart_items(user_id)

    if not items:
        raise CartError("Le panier est vide.")

    try:
        cursor = db.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (?, ?, ?)",
            (user_id, get_cart_total(user_id), "pending"),
        )
        order_id = int(cursor.lastrowid)

        for item in items:
            db.execute(
                """
                INSERT INTO orders_articles (order_id, article_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """,
                (order_id, item["article_id"], item["quantity"], item["price"]),
            )

        db.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
        db.commit()
    except sqlite3.Error:
        db.rollback()
        raise

    return order_id
