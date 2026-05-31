from __future__ import annotations

from flask import Blueprint, render_template, session

from app.core.security import login_required

from .cart_services import get_cart_items, get_cart_total

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
