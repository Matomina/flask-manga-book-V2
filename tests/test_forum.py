from __future__ import annotations


def assert_redirects_to_login(response) -> None:
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def _create_topic(
    db,
    user_id: int = 1,
    title: str = "Sujet test",
    message: str = "Contenu du sujet",
) -> int:
    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (user_id, title, message),
    )
    db.commit()

    return db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]


def _create_reply(
    db,
    topic_id: int,
    user_id: int = 1,
    message: str = "Réponse test",
) -> int:
    db.execute(
        """
        INSERT INTO replies (topic_id, user_id, message)
        VALUES (?, ?, ?)
        """,
        (topic_id, user_id, message),
    )
    db.commit()

    return db.execute(
        """
        SELECT id
        FROM replies
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]


# =========================
# FORUM PUBLIC
# =========================


def test_forum_page(client):
    response = client.get("/forum/")
    assert response.status_code == 200


def test_create_page_requires_login(client):
    response = client.get("/forum/create", follow_redirects=False)
    assert_redirects_to_login(response)


def test_create_page_authenticated(client, auth):
    auth.login_as_user()

    response = client.get("/forum/create")

    assert response.status_code == 200


def test_topic_detail_page(client, db):
    topic_id = _create_topic(db)

    response = client.get(f"/forum/{topic_id}")

    assert response.status_code == 200


def test_topic_detail_404(client):
    response = client.get("/forum/999999")

    assert response.status_code == 404


def test_create_topic_requires_login(client):
    response = client.post(
        "/forum/create",
        data={"title": "Sujet test", "message": "Bonjour"},
        follow_redirects=False,
    )

    assert_redirects_to_login(response)


def test_create_topic_invalid_redirects_without_insert(client, auth, db):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]

    response = client.post(
        "/forum/create",
        data={"title": "", "message": ""},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/forum/create")

    after = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]
    assert after == before


def test_create_topic_blank_values_after_strip_redirects_without_insert(
    client, auth, db
):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]

    response = client.post(
        "/forum/create",
        data={"title": "   ", "message": "   "},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/forum/create")

    after = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]
    assert after == before


def test_create_topic_authenticated_success(client, auth, db):
    auth.login_as_user()

    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    before = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]

    response = client.post(
        "/forum/create",
        data={
            "title": "Mon premier sujet",
            "message": "Contenu de mon sujet",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    after = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]
    assert after == before + 1

    created = db.execute(
        """
        SELECT id, user_id, title, message
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    assert created is not None
    assert created["user_id"] == user_id
    assert created["title"] == "Mon premier sujet"
    assert created["message"] == "Contenu de mon sujet"
    assert response.headers["Location"].endswith(f"/forum/{created['id']}")


def test_reply_requires_login(client, db):
    topic_id = _create_topic(db)

    response = client.post(
        f"/forum/{topic_id}/reply",
        data={"message": "Réponse test"},
        follow_redirects=False,
    )

    assert_redirects_to_login(response)


def test_reply_404_when_topic_does_not_exist(client, auth):
    auth.login_as_user()

    response = client.post(
        "/forum/999999/reply",
        data={"message": "Réponse test"},
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_reply_invalid_redirects_without_insert(client, auth, db):
    auth.login_as_user()
    topic_id = _create_topic(db)

    before = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]

    response = client.post(
        f"/forum/{topic_id}/reply",
        data={"message": ""},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/forum/{topic_id}")

    after = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]
    assert after == before


def test_reply_blank_value_after_strip_redirects_without_insert(client, auth, db):
    auth.login_as_user()
    topic_id = _create_topic(db)

    before = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]

    response = client.post(
        f"/forum/{topic_id}/reply",
        data={"message": "   "},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/forum/{topic_id}")

    after = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]
    assert after == before


def test_reply_authenticated_success(client, auth, db):
    auth.login_as_user()

    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    topic_id = _create_topic(db)

    before = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]

    response = client.post(
        f"/forum/{topic_id}/reply",
        data={"message": "Ma réponse"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/forum/{topic_id}")

    after = db.execute("SELECT COUNT(*) AS count FROM replies").fetchone()["count"]
    assert after == before + 1

    created = db.execute(
        """
        SELECT topic_id, user_id, message
        FROM replies
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    assert created is not None
    assert created["topic_id"] == topic_id
    assert created["user_id"] == user_id
    assert created["message"] == "Ma réponse"


# =========================
# FORUM ADMIN
# =========================


def test_admin_forum_list_requires_login(client):
    response = client.get("/admin/forum", follow_redirects=False)

    assert_redirects_to_login(response)


def test_admin_forum_list_forbidden_for_regular_user(client, auth):
    auth.login_as_user()

    response = client.get("/admin/forum", follow_redirects=False)

    assert response.status_code == 302
    assert "Location" in response.headers


def test_admin_forum_list_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/forum")

    assert response.status_code == 200


def test_admin_forum_detail_admin(client, auth, db):
    topic_id = _create_topic(db)

    auth.login_as_admin()

    response = client.get(f"/admin/forum/{topic_id}")

    assert response.status_code == 200


def test_admin_forum_detail_404(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/forum/999999")

    assert response.status_code == 404


def test_admin_forum_delete_topic_success(client, auth, db):
    topic_id = _create_topic(db)
    reply_id = _create_reply(db, topic_id=topic_id)

    auth.login_as_admin()

    response = client.post(
        f"/admin/forum/{topic_id}/delete",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/forum")

    deleted_topic = db.execute(
        """
        SELECT id
        FROM topics
        WHERE id = ?
        """,
        (topic_id,),
    ).fetchone()

    deleted_reply = db.execute(
        """
        SELECT id
        FROM replies
        WHERE id = ?
        """,
        (reply_id,),
    ).fetchone()

    assert deleted_topic is None
    assert deleted_reply is None


def test_admin_forum_delete_topic_404(client, auth):
    auth.login_as_admin()

    response = client.post(
        "/admin/forum/999999/delete",
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_admin_forum_delete_reply_success(client, auth, db):
    topic_id = _create_topic(db)
    reply_id = _create_reply(db, topic_id=topic_id)

    auth.login_as_admin()

    response = client.post(
        f"/admin/forum/replies/{reply_id}/delete",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith(f"/admin/forum/{topic_id}")

    deleted_reply = db.execute(
        """
        SELECT id
        FROM replies
        WHERE id = ?
        """,
        (reply_id,),
    ).fetchone()

    existing_topic = db.execute(
        """
        SELECT id
        FROM topics
        WHERE id = ?
        """,
        (topic_id,),
    ).fetchone()

    assert deleted_reply is None
    assert existing_topic is not None


def test_admin_forum_delete_reply_404(client, auth):
    auth.login_as_admin()

    response = client.post(
        "/admin/forum/replies/999999/delete",
        follow_redirects=False,
    )

    assert response.status_code == 404


def test_admin_forum_delete_reply_forbidden_for_regular_user(client, auth, db):
    topic_id = _create_topic(db)
    reply_id = _create_reply(db, topic_id=topic_id)

    auth.login_as_user()

    response = client.post(
        f"/admin/forum/replies/{reply_id}/delete",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "Location" in response.headers

    existing_reply = db.execute(
        """
        SELECT id
        FROM replies
        WHERE id = ?
        """,
        (reply_id,),
    ).fetchone()

    assert existing_reply is not None
