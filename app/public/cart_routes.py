from __future__ import annotations

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.core.security import login_required

from .cart_services import (
    CartError,
    add_cart_item,
    get_cart_items,
    get_cart_total,
    remove_cart_item,
    update_cart_item,
)
from .order_services import create_order_from_cart

bp = Blueprint("public_cart", __name__, template_folder="templates")


def _wants_json() -> bool:
    return (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.accept_mimetypes.best == "application/json"
        or request.is_json
    )


def _cart_payload(user_id: int) -> dict:
    items = get_cart_items(user_id)
    return {
        "items": [
            {
                "article_id": item["article_id"],
                "name": item["name"],
                "price": float(item["price"]),
                "quantity": item["quantity"],
                "stock": item["stock"],
                "image": url_for("static", filename=item["image"])
                if item["image"]
                else "",
            }
            for item in items
        ],
        "total": get_cart_total(user_id),
        "count": sum(item["quantity"] for item in items),
    }


def _quantity_from_request(default: str = "1") -> str:
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        return str(payload.get("quantity", default))
    return request.form.get("quantity", default)


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


@bp.get("/cart/data")
@login_required
def data():
    return jsonify(_cart_payload(session["user_id"]))


@bp.post("/cart/add/<int:article_id>")
@login_required
def add(article_id: int):
    try:
        add_cart_item(session["user_id"], article_id, _quantity_from_request())
    except CartError as exc:
        if _wants_json():
            return jsonify({"error": str(exc)}), 400
        raise

    if _wants_json():
        return jsonify(_cart_payload(session["user_id"]))
    return redirect(url_for("public_cart.cart"))


@bp.post("/cart/update/<int:article_id>")
@login_required
def update(article_id: int):
    try:
        update_cart_item(session["user_id"], article_id, _quantity_from_request())
    except CartError as exc:
        if _wants_json():
            return jsonify({"error": str(exc)}), 400
        raise

    if _wants_json():
        return jsonify(_cart_payload(session["user_id"]))
    return redirect(url_for("public_cart.cart"))


@bp.post("/cart/remove/<int:article_id>")
@login_required
def remove(article_id: int):
    remove_cart_item(session["user_id"], article_id)

    if _wants_json():
        return jsonify(_cart_payload(session["user_id"]))
    return redirect(url_for("public_cart.cart"))


@bp.post("/cart/checkout")
@login_required
def checkout():
    order_id = create_order_from_cart(session["user_id"])
    confirmation_url = url_for("public_cart.confirmation", order_id=order_id)

    if _wants_json():
        return jsonify({"redirect_url": confirmation_url})
    return redirect(confirmation_url)


@bp.route("/orders/<int:order_id>/confirmation")
@login_required
def confirmation(order_id: int):
    return render_template("public/order_confirmation.html", order_id=order_id)
