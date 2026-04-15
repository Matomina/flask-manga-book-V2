from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, url_for

from app.core.security import login_required
from .services import get_all_articles, get_article_by_id, get_featured_articles


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

    return render_template("public/article_detail.html", article=article)


@bp.route("/about")
def about():
    return render_template("public/about.html")


@bp.route("/contact", methods=["POST"])
@login_required
def contact():
    flash("Message envoyé.", "success")
    return redirect(url_for("public.home"))