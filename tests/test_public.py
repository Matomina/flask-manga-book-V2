from __future__ import annotations


def assert_redirects_to_login(response) -> None:
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


# =========================
# PAGES PUBLIQUES
# =========================


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_articles_page(client):
    response = client.get("/articles")
    assert response.status_code == 200


def test_article_detail_page(client):
    response = client.get("/articles/1")
    assert response.status_code == 200


def test_article_detail_404(client):
    response = client.get("/articles/999999")
    assert response.status_code == 404


def test_article_detail_anonymous_does_not_add_to_history(client, monkeypatch):
    called = {"value": False}

    def fake_add_to_history(user_id, article_id):
        called["value"] = True

    monkeypatch.setattr("app.public.routes.add_to_history", fake_add_to_history)

    response = client.get("/articles/1")

    assert response.status_code == 200
    assert called["value"] is False


def test_article_detail_authenticated_adds_to_history(client, auth, monkeypatch):
    captured = {}

    def fake_add_to_history(user_id, article_id):
        captured["user_id"] = user_id
        captured["article_id"] = article_id

    monkeypatch.setattr("app.public.routes.add_to_history", fake_add_to_history)

    auth.login_as_user()

    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    response = client.get("/articles/1")

    assert response.status_code == 200
    assert captured == {"user_id": user_id, "article_id": 1}


# =========================
# FAVORIS
# =========================


def test_favorites_requires_login(client):
    response = client.get("/favorites", follow_redirects=False)
    assert_redirects_to_login(response)


def test_add_to_favorites_requires_login(client):
    response = client.post("/favorites/add/1", follow_redirects=False)
    assert_redirects_to_login(response)


def test_remove_from_favorites_requires_login(client):
    response = client.post("/favorites/remove/1", follow_redirects=False)
    assert_redirects_to_login(response)


def test_favorites_page(client, auth):
    auth.login_as_user()

    response = client.get("/favorites")

    assert response.status_code == 200


def test_add_to_favorites_success(client, auth, monkeypatch):
    captured = {}

    def fake_add_favorite(user_id, article_id):
        captured["user_id"] = user_id
        captured["article_id"] = article_id

    monkeypatch.setattr("app.public.routes.add_favorite", fake_add_favorite)

    auth.login_as_user()

    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    response = client.post("/favorites/add/1", follow_redirects=False)

    assert response.status_code == 302
    assert "/articles/1" in response.headers["Location"]
    assert captured == {"user_id": user_id, "article_id": 1}


def test_add_to_favorites_404(client, auth, monkeypatch):
    monkeypatch.setattr("app.public.routes.get_article_by_id", lambda article_id: None)

    auth.login_as_user()
    response = client.post("/favorites/add/1", follow_redirects=False)

    assert response.status_code == 404


def test_remove_from_favorites_success(client, auth, monkeypatch):
    captured = {}

    def fake_remove_favorite(user_id, article_id):
        captured["user_id"] = user_id
        captured["article_id"] = article_id

    monkeypatch.setattr("app.public.routes.remove_favorite", fake_remove_favorite)

    auth.login_as_user()

    with client.session_transaction() as sess:
        user_id = sess["user_id"]

    response = client.post("/favorites/remove/1", follow_redirects=False)

    assert response.status_code == 302
    assert "/favorites" in response.headers["Location"]
    assert captured == {"user_id": user_id, "article_id": 1}


# =========================
# HISTORIQUE
# =========================


def test_history_requires_login(client):
    response = client.get("/history", follow_redirects=False)
    assert_redirects_to_login(response)


def test_history_page(client, auth):
    auth.login_as_user()

    response = client.get("/history")

    assert response.status_code == 200

    # =========================


# PROFIL
# =========================


def test_profile_requires_login(client):
    response = client.get("/profile", follow_redirects=False)

    assert_redirects_to_login(response)


def test_profile_page(client, auth):
    auth.login_as_user()

    response = client.get("/profile")

    assert response.status_code == 200


def test_profile_invalid_session_redirects_to_login(client, auth, monkeypatch):
    auth.login_as_user()

    monkeypatch.setattr("app.public.routes.get_user_by_id", lambda user_id: None)

    response = client.get("/profile", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


# =========================
# AUTRES PAGES
# =========================


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200


# =========================
# CONTACT / SUPPORT
# =========================


def test_contact_page_requires_login(client):
    response = client.get("/contact", follow_redirects=False)

    assert_redirects_to_login(response)


def test_contact_page_authenticated(client, auth):
    auth.login_as_user()

    response = client.get("/contact")

    assert response.status_code == 200


def test_contact_post_requires_login(client):
    response = client.post(
        "/contact",
        data={"sujet": "Commande", "message": "Bonjour"},
        follow_redirects=False,
    )

    assert_redirects_to_login(response)


def test_contact_authenticated(client, auth, db):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]

    response = client.post(
        "/contact",
        data={
            "sujet": "Test contact",
            "message": "Bonjour, ceci est un message de test.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact")

    after = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]
    assert after == before + 1

    created = db.execute(
        """
        SELECT sujet, message
        FROM contact
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    assert created is not None
    assert created["sujet"] == "Test contact"
    assert created["message"] == "Bonjour, ceci est un message de test."


def test_contact_invalid_redirects_contact_without_insert(client, auth, db):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]

    response = client.post(
        "/contact",
        data={
            "sujet": "",
            "message": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact")

    after = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]
    assert after == before


def test_contact_blank_values_after_strip_redirects_contact_without_insert(
    client,
    auth,
    db,
):
    auth.login_as_user()

    before = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]

    response = client.post(
        "/contact",
        data={
            "sujet": "   ",
            "message": "   ",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/contact")

    after = db.execute("SELECT COUNT(*) AS count FROM contact").fetchone()["count"]
    assert after == before
