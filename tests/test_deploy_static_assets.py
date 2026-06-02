from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_ROOT / "app" / "static"
MINIMUM_DEMO_ARTICLES = 24
ARTICLE_CARD_MARKUP = b'class="article-card product-card card"'


def test_all_seeded_article_images_exist(db):
    rows = db.execute(
        """
        SELECT id, name, image
        FROM articles
        WHERE image IS NOT NULL AND image != ''
        ORDER BY id
        """
    ).fetchall()

    missing_images = [
        f"#{row['id']} {row['name']} -> {row['image']}"
        for row in rows
        if not (STATIC_DIR / row["image"]).is_file()
    ]

    assert missing_images == []


def test_demo_catalog_contains_expected_minimum_articles(db):
    row = db.execute("SELECT COUNT(*) AS total FROM articles").fetchone()

    assert row is not None
    assert row["total"] >= MINIMUM_DEMO_ARTICLES


def test_catalog_page_renders_all_seeded_articles(client, db):
    article_count = db.execute("SELECT COUNT(*) AS total FROM articles").fetchone()
    response = client.get("/articles")

    assert article_count is not None
    assert response.status_code == 200
    assert response.data.count(ARTICLE_CARD_MARKUP) == article_count["total"]
    assert str(article_count["total"]).encode() in response.data
    assert "article".encode() in response.data
    assert "trouv".encode() in response.data
