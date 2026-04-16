from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.core.security import login_required
from .services import (
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

bp = Blueprint(
    "public",
    __name__,
    template_folder="templates",
)


@bp.route("/")
def home():
    featured_articles = get_featured_articles()
    return render_template("public/home.html", articles=featured_articles)


@bp.route("/articles")
def articles():
    articles_list = get_all_articles()
    return render_template("public/articles.html", articles=articles_list)


@bp.route("/articles/<int:article_id>")
def article_detail(article_id: int):
    article = get_article_by_id(article_id)

    if article is None:
        abort(404)

    if session.get("user_id"):
        add_to_history(session["user_id"], article_id)

    return render_template("public/article_detail.html", article=article)


# =========================
# FAVORIS
# =========================

@bp.route("/favorites")
@login_required
def favorites():
    user_id = session["user_id"]
    favorite_articles = get_user_favorites(user_id)
    return render_template("public/favorites.html", articles=favorite_articles)


@bp.route("/favorites/add/<int:article_id>", methods=["POST"])
@login_required
def add_to_favorites(article_id: int):
    article = get_article_by_id(article_id)

    if article is None:
        abort(404)

    add_favorite(session["user_id"], article_id)
    flash("Article ajouté aux favoris.", "success")
    return redirect(url_for("public.article_detail", article_id=article_id))


@bp.route("/favorites/remove/<int:article_id>", methods=["POST"])
@login_required
def remove_from_favorites(article_id: int):
    remove_favorite(session["user_id"], article_id)
    flash("Article retiré des favoris.", "info")
    return redirect(url_for("public.favorites"))


# =========================
# HISTORIQUE
# =========================

@bp.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    history_articles = get_user_history(user_id)
    return render_template("public/history.html", articles=history_articles)


# =========================
# AUTRES
# =========================

@bp.route("/about")
def about():
    return render_template("public/about.html")


@bp.route("/contact", methods=["POST"])
@login_required
def contact():
    sujet = request.form.get("sujet", "").strip()
    message = request.form.get("message", "").strip()

    if not sujet or not message:
        flash("Veuillez remplir le sujet et le message.", "warning")
        return redirect(url_for("public.home"))

    create_contact_message(session["user_id"], sujet, message)
    flash("Message envoyé.", "success")
    return redirect(url_for("public.home"))