from __future__ import annotations


def assert_redirects_to_login(response) -> None:
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_forum_page(client):
    response = client.get("/forum/")
    assert response.status_code == 200


def test_topic_detail_page(client, db):
    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (1, "Sujet test", "Contenu du sujet"),
    )
    db.commit()

    topic_id = db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]

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
    assert response.headers["Location"].endswith("/forum/")

    after = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]
    assert after == before


def test_create_topic_blank_values_after_strip_redirects_without_insert(client, auth, db):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM topics").fetchone()["count"]

    response = client.post(
        "/forum/create",
        data={"title": "   ", "message": "   "},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/forum/")

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
    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (1, "Sujet test", "Contenu du sujet"),
    )
    db.commit()

    topic_id = db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]

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

    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (1, "Sujet test", "Contenu du sujet"),
    )
    db.commit()

    topic_id = db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]

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

    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (1, "Sujet test", "Contenu du sujet"),
    )
    db.commit()

    topic_id = db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]

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

    db.execute(
        """
        INSERT INTO topics (user_id, title, message)
        VALUES (?, ?, ?)
        """,
        (1, "Sujet test", "Contenu du sujet"),
    )
    db.commit()

    topic_id = db.execute(
        """
        SELECT id
        FROM topics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()["id"]

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