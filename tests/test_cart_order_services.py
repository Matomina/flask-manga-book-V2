from __future__ import annotations

import pytest

from app.public.cart_services import (
    CartError,
    add_cart_item,
    get_cart_items,
    get_cart_total,
    remove_cart_item,
    update_cart_item,
)
from app.public.favorite_services import toggle_favorite
from app.public.order_services import create_order_from_cart


def test_add_cart_item_creates_item(app, db):
    with app.app_context():
        add_cart_item(user_id=2, article_id=1, quantity=2)
        items = get_cart_items(user_id=2)

    assert len(items) == 1
    assert items[0]["article_id"] == 1
    assert items[0]["quantity"] == 2


def test_add_cart_item_accumulates_quantity(app):
    with app.app_context():
        add_cart_item(user_id=2, article_id=1, quantity=1)
        add_cart_item(user_id=2, article_id=1, quantity=2)
        items = get_cart_items(user_id=2)

    assert len(items) == 1
    assert items[0]["quantity"] == 3


def test_add_cart_item_rejects_invalid_quantity(app):
    with app.app_context(), pytest.raises(CartError, match="Quantité invalide"):
        add_cart_item(user_id=2, article_id=1, quantity=0)


def test_add_cart_item_rejects_missing_article(app):
    with app.app_context(), pytest.raises(CartError, match="Article introuvable"):
        add_cart_item(user_id=2, article_id=999999, quantity=1)


def test_update_cart_item_updates_quantity(app):
    with app.app_context():
        add_cart_item(user_id=2, article_id=1, quantity=1)
        update_cart_item(user_id=2, article_id=1, quantity=3)
        items = get_cart_items(user_id=2)

    assert items[0]["quantity"] == 3


def test_update_cart_item_rejects_missing_cart_line(app):
    with app.app_context(), pytest.raises(CartError, match="Article absent du panier"):
        update_cart_item(user_id=2, article_id=1, quantity=1)


def test_remove_cart_item_deletes_item(app):
    with app.app_context():
        add_cart_item(user_id=2, article_id=1, quantity=1)
        remove_cart_item(user_id=2, article_id=1)
        items = get_cart_items(user_id=2)

    assert items == []


def test_get_cart_total_returns_rounded_total(app):
    with app.app_context():
        add_cart_item(user_id=2, article_id=1, quantity=2)
        items = get_cart_items(user_id=2)
        expected = round(float(items[0]["price"] * 2), 2)
        total = get_cart_total(user_id=2)

    assert total == expected


def test_create_order_from_cart_creates_order_and_clears_cart(app, db):
    with app.app_context():
        before_stock = db.execute(
            "SELECT stock FROM articles WHERE id = ?",
            (1,),
        ).fetchone()["stock"]
        add_cart_item(user_id=2, article_id=1, quantity=2)

        order_id = create_order_from_cart(user_id=2)

        order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        order_item = db.execute(
            "SELECT * FROM orders_articles WHERE order_id = ?",
            (order_id,),
        ).fetchone()
        after_stock = db.execute(
            "SELECT stock FROM articles WHERE id = ?",
            (1,),
        ).fetchone()["stock"]
        cart_items = get_cart_items(user_id=2)

    assert order is not None
    assert order["status"] == "pending"
    assert order_item is not None
    assert order_item["article_id"] == 1
    assert order_item["quantity"] == 2
    assert after_stock == before_stock - 2
    assert cart_items == []


def test_create_order_from_empty_cart_raises(app):
    with app.app_context(), pytest.raises(CartError, match="Le panier est vide"):
        create_order_from_cart(user_id=2)


def test_toggle_favorite_adds_then_removes(app, db):
    with app.app_context():
        added = toggle_favorite(user_id=2, article_id=1)
        favorite = db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND article_id = ?",
            (2, 1),
        ).fetchone()
        removed = toggle_favorite(user_id=2, article_id=1)
        deleted = db.execute(
            "SELECT id FROM favorites WHERE user_id = ? AND article_id = ?",
            (2, 1),
        ).fetchone()

    assert added == "added"
    assert favorite is not None
    assert removed == "removed"
    assert deleted is None


def test_cart_items_schema_has_expected_constraints(app, db):
    with app.app_context():
        table = db.execute(
            """
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table' AND name = 'cart_items'
            """
        ).fetchone()
        foreign_keys = db.execute("PRAGMA foreign_key_list(cart_items)").fetchall()
        indexes = db.execute("PRAGMA index_list(cart_items)").fetchall()

    assert table is not None
    assert "CHECK (quantity > 0)" in table["sql"]
    assert {foreign_key["table"] for foreign_key in foreign_keys} == {"articles", "user"}
    assert {index["name"] for index in indexes} >= {
        "idx_cart_items_article_id",
        "idx_cart_items_user_id",
    }
