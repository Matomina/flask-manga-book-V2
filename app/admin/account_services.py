from __future__ import annotations

from app.db import get_db


def get_all_users_admin():
    db = get_db()
    sql = """
        SELECT id, first_name, last_name, email, phone, address, city, role, created_at
        FROM user
        ORDER BY created_at DESC, id DESC
    """
    return db.execute(sql).fetchall()


def get_user_by_id_admin(user_id: int):
    db = get_db()
    sql = """
        SELECT id, first_name, last_name, email, phone, address, city, role, created_at
        FROM user
        WHERE id = ?
    """
    return db.execute(sql, (user_id,)).fetchone()
