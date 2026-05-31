from __future__ import annotations

from app.admin.services import delete_contact


def _insert_contact(db, *, sujet: str = "Contact delete test") -> int:
    cursor = db.execute(
        """
        INSERT INTO contact (user_id, sujet, message, status)
        VALUES (?, ?, ?, ?)
        """,
        (2, sujet, "Message à supprimer.", "pending"),
    )
    db.commit()
    return int(cursor.lastrowid)


def test_delete_contact_removes_contact(app, db):
    with app.app_context():
        contact_id = _insert_contact(db)

        deleted = delete_contact(contact_id)

        contact = db.execute(
            "SELECT id FROM contact WHERE id = ?",
            (contact_id,),
        ).fetchone()

    assert deleted is True
    assert contact is None


def test_delete_contact_returns_false_when_missing(app):
    with app.app_context():
        deleted = delete_contact(999999)

    assert deleted is False


def test_admin_contact_delete_requires_login(client, db):
    contact_id = _insert_contact(db)

    response = client.post(
        f"/admin/contact/{contact_id}/delete",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_contact_delete_success(client, auth, db):
    contact_id = _insert_contact(db)

    auth.login_as_admin()
    response = client.post(
        f"/admin/contact/{contact_id}/delete",
        follow_redirects=False,
    )

    contact = db.execute(
        "SELECT id FROM contact WHERE id = ?",
        (contact_id,),
    ).fetchone()

    assert response.status_code == 302
    assert "/admin/contact" in response.headers["Location"]
    assert contact is None


def test_admin_contact_delete_404(client, auth):
    auth.login_as_admin()

    response = client.post(
        "/admin/contact/999999/delete",
        follow_redirects=False,
    )

    assert response.status_code == 404
