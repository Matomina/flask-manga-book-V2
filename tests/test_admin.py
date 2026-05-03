from __future__ import annotations

from io import BytesIO

from app.admin.services import get_dashboard_stats


def test_admin_requires_login(client):
    response = client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_dashboard_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/")

    assert response.status_code == 200


def test_admin_dashboard_displays_enriched_stats(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Messages non lus" in html
    assert "Articles en stock faible" in html
    assert "Articles sans stock" in html
    assert "Sujets forum" in html
    assert "Réponses forum" in html


def test_get_dashboard_stats_contains_enriched_keys(app):
    with app.app_context():
        stats = get_dashboard_stats()

    expected_keys = {
        "users",
        "articles",
        "orders",
        "contacts",
        "unread_contacts",
        "forum_topics",
        "forum_replies",
        "low_stock_articles",
        "out_of_stock_articles",
    }

    assert expected_keys.issubset(stats.keys())


def test_get_dashboard_stats_counts_stock_alerts(app, db):
    with app.app_context():
        before = get_dashboard_stats()

        db.execute(
            """
            INSERT INTO articles (name, genres, universe, image, price, stock, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Article stock faible test",
                "manga",
                "naruto",
                "uploads/low-stock-test.webp",
                9.90,
                5,
                "Lundi",
            ),
        )

        db.execute(
            """
            INSERT INTO articles (name, genres, universe, image, price, stock, release_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "Article rupture stock test",
                "goodies",
                "dragon_ball",
                "uploads/out-stock-test.webp",
                14.90,
                0,
                "Mardi",
            ),
        )

        db.commit()

        after = get_dashboard_stats()

    assert after["low_stock_articles"] == before["low_stock_articles"] + 1
    assert after["out_of_stock_articles"] == before["out_of_stock_articles"] + 1


def test_admin_forbidden_for_regular_user(client, auth):
    auth.login_as_user()

    response = client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert "Location" in response.headers


def test_admin_contact_list_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/contact")

    assert response.status_code == 200


def test_admin_contact_detail_marks_as_read(client, auth, db):
    before = db.execute(
        "SELECT status FROM contact WHERE id = ?",
        (1,),
    ).fetchone()
    assert before is not None
    assert before["status"] != "read"

    auth.login_as_admin()
    response = client.get("/admin/contact/1")

    assert response.status_code == 200

    after = db.execute(
        "SELECT status FROM contact WHERE id = ?",
        (1,),
    ).fetchone()
    assert after is not None
    assert after["status"] == "read"


def test_admin_contact_detail_404(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/contact/999999")

    assert response.status_code == 404


def test_admin_articles_list_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles")

    assert response.status_code == 200


def test_admin_article_create_page_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles/create")

    assert response.status_code == 200


def test_admin_article_detail_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles/1")

    assert response.status_code == 200


def test_admin_article_detail_404(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles/999999")

    assert response.status_code == 404


def test_admin_article_create_success(client, auth, db, monkeypatch):
    auth.login_as_admin()

    monkeypatch.setattr(
        "app.admin.routes.save_image",
        lambda _file: "uploads/test-image.webp",
    )

    response = client.post(
        "/admin/articles/create",
        data={
            "name": "Bleach Tome 1",
            "genres": "manga",
            "universe": "",
            "price": "7.90",
            "stock": "12",
            "release_day": "Vendredi",
            "image": (BytesIO(b"fake-image"), "bleach.webp"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/admin/articles" in response.headers["Location"]

    article = db.execute(
        """
        SELECT name, genres, universe, image, price, stock, release_day
        FROM articles
        WHERE name = ?
        """,
        ("Bleach Tome 1",),
    ).fetchone()

    assert article is not None
    assert article["name"] == "Bleach Tome 1"
    assert article["genres"] == "manga"
    assert article["universe"] is None
    assert article["image"] == "uploads/test-image.webp"
    assert article["stock"] == 12
    assert article["release_day"] == "Vendredi"


def test_admin_article_create_invalid_returns_400(client, auth, db):
    auth.login_as_admin()

    count_before = db.execute("SELECT COUNT(*) AS count FROM articles").fetchone()[
        "count"
    ]

    response = client.post(
        "/admin/articles/create",
        data={
            "name": "",
            "genres": "invalide",
            "universe": "",
            "price": "-5",
            "stock": "abc",
            "release_day": "Jour invalide",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    count_after = db.execute("SELECT COUNT(*) AS count FROM articles").fetchone()[
        "count"
    ]

    assert count_after == count_before


def test_admin_article_create_invalid_image_format_returns_400(
    client,
    auth,
    db,
    monkeypatch,
):
    auth.login_as_admin()

    count_before = db.execute("SELECT COUNT(*) AS count FROM articles").fetchone()[
        "count"
    ]

    monkeypatch.setattr("app.admin.routes.save_image", lambda _file: None)

    response = client.post(
        "/admin/articles/create",
        data={
            "name": "Produit test",
            "genres": "manga",
            "universe": "",
            "price": "9.90",
            "stock": "5",
            "release_day": "Lundi",
            "image": (BytesIO(b"not-an-image"), "document.txt"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert response.status_code == 400

    count_after = db.execute("SELECT COUNT(*) AS count FROM articles").fetchone()[
        "count"
    ]

    assert count_after == count_before


def test_admin_article_edit_page_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles/1/edit")

    assert response.status_code == 200


def test_admin_article_edit_success_without_new_image(client, auth, db):
    original = db.execute(
        """
        SELECT id, image
        FROM articles
        WHERE id = ?
        """,
        (1,),
    ).fetchone()

    assert original is not None

    auth.login_as_admin()
    response = client.post(
        "/admin/articles/1/edit",
        data={
            "name": "Lunette Gojo Premium",
            "genres": "goodies",
            "universe": "jujutsu_kaisen",
            "price": "59.90",
            "stock": "8",
            "release_day": "Sans jour fixe",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/admin/articles/1" in response.headers["Location"]

    updated = db.execute(
        """
        SELECT name, genres, universe, image, price, stock, release_day
        FROM articles
        WHERE id = ?
        """,
        (1,),
    ).fetchone()

    assert updated is not None
    assert updated["name"] == "Lunette Gojo Premium"
    assert updated["genres"] == "goodies"
    assert updated["universe"] == "jujutsu_kaisen"
    assert updated["image"] == original["image"]
    assert updated["stock"] == 8
    assert updated["release_day"] == "Sans jour fixe"


def test_admin_article_edit_invalid_returns_400(client, auth, db):
    before = db.execute(
        "SELECT name FROM articles WHERE id = ?",
        (1,),
    ).fetchone()
    assert before is not None

    auth.login_as_admin()
    response = client.post(
        "/admin/articles/1/edit",
        data={
            "name": "",
            "genres": "invalide",
            "universe": "",
            "price": "-1",
            "stock": "abc",
            "release_day": "Jour invalide",
        },
        follow_redirects=False,
    )

    assert response.status_code == 400

    after = db.execute(
        "SELECT name FROM articles WHERE id = ?",
        (1,),
    ).fetchone()
    assert after is not None
    assert after["name"] == before["name"]


def test_admin_article_edit_404(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/articles/999999/edit")

    assert response.status_code == 404


def test_admin_article_delete_success(client, auth, db, monkeypatch):
    auth.login_as_admin()

    monkeypatch.setattr(
        "app.admin.routes.save_image",
        lambda _file: "uploads/delete-test.webp",
    )

    create_response = client.post(
        "/admin/articles/create",
        data={
            "name": "Article à supprimer",
            "genres": "manga",
            "universe": "",
            "price": "8.90",
            "stock": "3",
            "release_day": "Lundi",
            "image": (BytesIO(b"fake-image"), "delete.webp"),
        },
        content_type="multipart/form-data",
        follow_redirects=False,
    )

    assert create_response.status_code == 302

    article = db.execute(
        "SELECT id FROM articles WHERE name = ?",
        ("Article à supprimer",),
    ).fetchone()
    assert article is not None

    response = client.post(
        f"/admin/articles/{article['id']}/delete",
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/admin/articles" in response.headers["Location"]

    deleted = db.execute(
        "SELECT id FROM articles WHERE id = ?",
        (article["id"],),
    ).fetchone()
    assert deleted is None


def test_admin_article_delete_404(client, auth):
    auth.login_as_admin()

    response = client.post("/admin/articles/999999/delete", follow_redirects=False)

    assert response.status_code == 404
