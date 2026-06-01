from __future__ import annotations

import sqlite3
from typing import Any

from app.db import get_db

VALID_ORDER_STATUSES = {"pending", "paid", "shipped", "delivered", "cancelled"}


def _normalize_str(value: Any) -> str:
    return str(value or "").strip()


def get_all_orders_admin(status_filter: str = "all") -> list[sqlite3.Row]:
    db = get_db()
    where_sql = ""
    params: tuple[str, ...] = ()

    if status_filter in VALID_ORDER_STATUSES:
        where_sql = "WHERE o.status = ?"
        params = (status_filter,)

    return db.execute(
        f"""
        SELECT
            o.id,
            o.user_id,
            o.total_amount,
            o.status,
            o.created_at,
            u.first_name,
            u.last_name,
            u.email,
            COUNT(oa.id) AS items_count
        FROM orders AS o
        LEFT JOIN user AS u ON u.id = o.user_id
        LEFT JOIN orders_articles AS oa ON oa.order_id = o.id
        {where_sql}
        GROUP BY o.id
        ORDER BY o.created_at DESC, o.id DESC
        """,
        params,
    ).fetchall()


def get_order_by_id_admin(order_id: int) -> sqlite3.Row | None:
    db = get_db()
    return db.execute(
        """
        SELECT
            o.id,
            o.user_id,
            o.total_amount,
            o.status,
            o.created_at,
            u.email,
            u.first_name,
            u.last_name,
            u.phone,
            u.address,
            u.city
        FROM orders AS o
        LEFT JOIN user AS u ON u.id = o.user_id
        WHERE o.id = ?
        """,
        (order_id,),
    ).fetchone()


def get_order_items_by_order_id(order_id: int) -> list[sqlite3.Row]:
    db = get_db()
    return db.execute(
        """
        SELECT
            oa.id,
            oa.order_id,
            oa.article_id,
            oa.quantity,
            oa.unit_price,
            a.name,
            a.genres,
            a.universe,
            a.image
        FROM orders_articles AS oa
        JOIN articles AS a ON a.id = oa.article_id
        WHERE oa.order_id = ?
        ORDER BY oa.id ASC
        """,
        (order_id,),
    ).fetchall()


def update_order_status_admin(order_id: int, status: str) -> bool:
    normalized_status = _normalize_str(status)

    if normalized_status not in VALID_ORDER_STATUSES:
        raise ValueError("Statut de commande invalide.")

    db = get_db()
    cursor = db.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (normalized_status, order_id),
    )
    db.commit()
    return cursor.rowcount > 0
