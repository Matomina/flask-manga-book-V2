from __future__ import annotations


def _insert_topic(db, *, title: str = "Sujet réponse admin test") -> int:
    cursor = db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (2, title, "Message initial du sujet."),
    )
    db.commit()
    return int(cursor.lastrowid)


def test_admin_forum_detail_displays_reply_form(client, auth, db):
    topic_id = _insert_topic(db)

    auth.login_as_admin()
    response = client.get(f"/admin/forum/{topic_id}")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Répondre en tant qu’admin" in html
    assert "Message de réponse" in html
    assert f"/admin/forum/{topic_id}/replies" in html
    assert "Publier la réponse admin" in html


def test_admin_forum_create_reply_requires_login(client, db):
    topic_id = _insert_topic(db)

    response = client.post(
        f"/admin/forum/{topic_id}/replies",
        data={"message": "Réponse sans session."},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_forum_create_reply_success(client, auth, db):
    topic_id = _insert_topic(db)

    auth.login_as_admin()
    response = client.post(
        f"/admin/forum/{topic_id}/replies",
        data={"message": "Réponse officielle de l’équipe admin."},
        follow_redirects=False,
    )

    reply = db.execute(
        """
        SELECT topic_id, user_id, message
        FROM replies
        WHERE topic_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (topic_id,),
    ).fetchone()

    assert response.status_code == 302
    assert f"/admin/forum/{topic_id}" in response.headers["Location"]
    assert reply is not None
    assert reply["topic_id"] == topic_id
    assert reply["message"] == "Réponse officielle de l’équipe admin."


def test_admin_forum_create_reply_empty_message_returns_400(
    client,
    auth,
    db,
):
    topic_id = _insert_topic(db)

    auth.login_as_admin()
    response = client.post(
        f"/admin/forum/{topic_id}/replies",
        data={"message": "   "},
        follow_redirects=False,
    )

    count = db.execute(
        "SELECT COUNT(*) AS count FROM replies WHERE topic_id = ?",
        (topic_id,),
    ).fetchone()

    assert response.status_code == 400
    assert count is not None
    assert count["count"] == 0


def test_admin_forum_create_reply_404(client, auth):
    auth.login_as_admin()

    response = client.post(
        "/admin/forum/999999/replies",
        data={"message": "Réponse impossible."},
        follow_redirects=False,
    )

    assert response.status_code == 404
