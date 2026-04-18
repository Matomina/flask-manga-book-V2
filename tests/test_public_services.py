from __future__ import annotations

from app.public.services import (
    add_favorite,
    add_to_history,
    create_contact_message,
    get_all_articles,
    get_article_by_id,
    get_featured_articles,
    get_user_favorites,
    get_user_history,
    remove_favorite,
)


def test_get_all_articles(db, app):
    with app.app_context():
        articles = get_all_articles()

    assert len(articles) > 0
    assert "id" in articles[0].keys()
    assert "name" in articles[0].keys()


def test_get_featured_articles_limit(db, app):
    with app.app_context():
        articles = get_featured_articles(limit=3)

    assert len(articles) == 3


def test_get_article_by_id_found(db, app):
    with app.app_context():
        article = get_article_by_id(1)

    assert article is not None
    assert article["id"] == 1


def test_get_article_by_id_not_found(db, app):
    with app.app_context():
        article = get_article_by_id(999999)

    assert article is None


def test_add_and_remove_favorite(db, app):
    with app.app_context():
        add_favorite(2, 1)

        favorite = db.execute(
            """
            SELECT user_id, article_id
            FROM favorites
            WHERE user_id = ? AND article_id = ?
            """,
            (2, 1),
        ).fetchone()

        assert favorite is not None

        remove_favorite(2, 1)

        favorite = db.execute(
            """
            SELECT user_id, article_id
            FROM favorites
            WHERE user_id = ? AND article_id = ?
            """,
            (2, 1),
        ).fetchone()

        assert favorite is None


def test_get_user_favorites(db, app):
    with app.app_context():
        add_favorite(2, 1)
        favorites = get_user_favorites(2)

    assert len(favorites) >= 1
    assert any(article["id"] == 1 for article in favorites)


def test_add_to_history_insert_and_get_user_history(db, app):
    with app.app_context():
        add_to_history(2, 1)
        history = get_user_history(2)

    assert len(history) >= 1
    assert any(article["id"] == 1 for article in history)


def test_add_to_history_upsert_does_not_duplicate(db, app):
    with app.app_context():
        add_to_history(2, 1)
        add_to_history(2, 1)

        rows = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM history
            WHERE user_id = ? AND article_id = ?
            """,
            (2, 1),
        ).fetchone()

    assert rows["count"] == 1


def test_create_contact_message(db, app):
    with app.app_context():
        before = db.execute(
            "SELECT COUNT(*) AS count FROM contact"
        ).fetchone()["count"]

        create_contact_message(2, "Sujet test", "Message test")

        after = db.execute(
            "SELECT COUNT(*) AS count FROM contact"
        ).fetchone()["count"]

        created = db.execute(
            """
            SELECT user_id, sujet, message
            FROM contact
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    assert after == before + 1
    assert created is not None
    assert created["user_id"] == 2
    assert created["sujet"] == "Sujet test"
    assert created["message"] == "Message test"