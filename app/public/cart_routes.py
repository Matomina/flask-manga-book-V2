from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.core.security import login_required

from .cart_services import add_cart_item, get_cart_items, get_cart_total

bp = Blueprint("public_cart", __name__, template_folder="templates")


@bp.route("/cart")
@bp.route("/panier")
@login_required
def cart():
    user_id = session["user_id"]
    return render_template(
        "public/cart.html",
        cart_items=get_cart_items(user_id),
        cart_total=get_cart_total(user_id),
    )


@bp.post("/cart/add/<int:article_id>")
@login_required
def add(article_id: int):
    add_cart_item(session["user_id"], article_id, request.form.get("quantity", "1"))
    return redirect(url_for("public_cart.cart"))
