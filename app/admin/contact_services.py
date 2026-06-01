from __future__ import annotations

import sqlite3

from app.db import get_db


def get_all_contacts(status_filter: str = "all") -> list[sqlite3.Row]:
    db = get_db()
    where_sql = ""

    if status_filter == "unread":
        where_sql = "WHERE c.status != 'read'"
    elif status_filter == "read":
        where_sql = "WHERE c.status = 'read'"

    return db.execute(
        f"""
        SELECT c.id, c.sujet, c.message, c.status, c.created_at, u.email
        FROM contact AS c
        LEFT JOIN user AS u ON u.id = c.user_id
        {where_sql}
        ORDER BY c.created_at DESC, c.id DESC
        """
    ).fetchall()


def get_contact_by_id(contact_id: int) -> sqlite3.Row | None:
    db = get_db()
    return db.execute(
        """
        SELECT c.id, c.sujet, c.message, c.status, c.created_at, u.email
        FROM contact AS c
        LEFT JOIN user AS u ON u.id = c.user_id
        WHERE c.id = ?
        """,
        (contact_id,),
    ).fetchone()


def mark_contact_as_read(contact_id: int) -> None:
    db = get_db()
    db.execute(
        "UPDATE contact SET status = 'read' WHERE id = ?",
        (contact_id,),
    )
    db.commit()


def delete_contact(contact_id: int) -> bool:
    db = get_db()
    cursor = db.execute(
        "DELETE FROM contact WHERE id = ?",
        (contact_id,),
    )
    db.commit()
    return cursor.rowcount > 0
