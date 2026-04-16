from __future__ import annotations

from flask import Blueprint, abort, render_template

from app.core.security import admin_required
from .services import (
    get_dashboard_stats,
    get_all_contacts,
    get_contact_by_id,
    mark_contact_as_read,
    get_all_articles_admin,
    get_article_by_id_admin,
    create_article,
    update_article,
    delete_article,
)

bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


# =========================
# DASHBOARD
# =========================

@bp.route("/", methods=["GET"])
@admin_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template("admin/dashboard.html", stats=stats)


# =========================
# CONTACTS
# =========================

@bp.route("/contact", methods=["GET"])
@admin_required
def contact_list():
    messages = get_all_contacts()
    return render_template("admin/contact_list.html", messages=messages)


@bp.route("/contact/<int:contact_id>", methods=["GET"])
@admin_required
def contact_detail(contact_id: int):
    message = get_contact_by_id(contact_id)

    if message is None:
        abort(404)

    mark_contact_as_read(contact_id)

    return render_template("admin/contact_detail.html", message=message)

@bp.route("/articles")
@admin_required
def articles_list():
    articles = get_all_articles_admin()
    return render_template("admin/articles_list.html", articles=articles)

@bp.route("/articles/create", methods=["GET", "POST"])
@admin_required
def article_create():
    if request.method == "POST":
        data = request.form.to_dict()

        create_article(data)
        flash("Article créé.", "success")

        return redirect(url_for("admin.articles_list"))

    return render_template("admin/article_form.html")

@bp.route("/articles/edit/<int:article_id>", methods=["GET", "POST"])
@admin_required
def article_edit(article_id: int):
    article = get_article_by_id_admin(article_id)

    if article is None:
        abort(404)

    if request.method == "POST":
        data = request.form.to_dict()

        update_article(article_id, data)
        flash("Article modifié.", "success")

        return redirect(url_for("admin.articles_list"))

    return render_template("admin/article_form.html", article=article)

@bp.route("/articles/delete/<int:article_id>", methods=["POST"])
@admin_required
def article_delete(article_id: int):
    delete_article(article_id)
    flash("Article supprimé.", "info")

    return redirect(url_for("admin.articles_list"))