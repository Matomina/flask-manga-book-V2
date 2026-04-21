from __future__ import annotations

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.core.security import admin_required
from app.forum.services import (
    delete_reply_by_id,
    delete_topic_by_id,
    get_all_topics_for_admin,
    get_replies_by_topic_id,
    get_reply_by_id,
    get_topic_by_id,
)
from .services import (
    create_article,
    delete_article,
    get_all_articles_admin,
    get_all_contacts,
    get_article_by_id_admin,
    get_contact_by_id,
    get_dashboard_stats,
    mark_contact_as_read,
    save_image,
    update_article,
    validate_article_data,
)

bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
)


# =========================
# HELPERS
# =========================

def _flash_errors(errors: list[str]) -> None:
    """Afficher une liste d'erreurs dans les messages flash."""
    for error in errors:
        flash(error, "danger")


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
    return render_template("admin/contacts/list.html", messages=messages)


@bp.route("/contact/<int:contact_id>", methods=["GET"])
@admin_required
def contact_detail(contact_id: int):
    message = get_contact_by_id(contact_id)

    if message is None:
        abort(404)

    if message["status"] != "read":
        mark_contact_as_read(contact_id)
        message = get_contact_by_id(contact_id)

    return render_template("admin/contacts/detail.html", message=message)


# =========================
# ARTICLES
# =========================

@bp.route("/articles", methods=["GET"])
@admin_required
def articles_list():
    articles = get_all_articles_admin()
    return render_template("admin/articles/list.html", articles=articles)


@bp.route("/articles/create", methods=["GET", "POST"])
@admin_required
def article_create():
    if request.method == "POST":
        data = request.form.to_dict()
        uploaded_file = request.files.get("image")
        image_path = save_image(uploaded_file)

        errors: list[str] = []

        if uploaded_file is not None and uploaded_file.filename and image_path is None:
            errors.append(
                "Format d'image invalide. Extensions autorisées : png, jpg, jpeg, webp."
            )
        elif image_path is not None:
            data["image"] = image_path

        clean_data, validation_errors = validate_article_data(data, require_image=True)
        errors.extend(validation_errors)

        if errors:
            _flash_errors(errors)
            return render_template("admin/articles/create.html", data=data), 400

        create_article(clean_data)
        flash("Article créé avec succès.", "success")
        return redirect(url_for("admin.articles_list"))

    return render_template("admin/articles/create.html")


@bp.route("/articles/<int:article_id>", methods=["GET"])
@admin_required
def article_detail(article_id: int):
    article = get_article_by_id_admin(article_id)

    if article is None:
        abort(404)

    return render_template("admin/articles/detail.html", article=article)


@bp.route("/articles/<int:article_id>/edit", methods=["GET", "POST"])
@admin_required
def article_edit(article_id: int):
    article = get_article_by_id_admin(article_id)

    if article is None:
        abort(404)

    if request.method == "POST":
        data = request.form.to_dict()
        uploaded_file = request.files.get("image")
        image_path = save_image(uploaded_file)

        errors: list[str] = []

        if uploaded_file is not None and uploaded_file.filename and image_path is None:
            errors.append(
                "Format d'image invalide. Extensions autorisées : png, jpg, jpeg, webp."
            )
        elif image_path is not None:
            data["image"] = image_path

        clean_data, validation_errors = validate_article_data(data, require_image=False)
        errors.extend(validation_errors)

        if not clean_data["image"]:
            clean_data["image"] = article["image"]

        if errors:
            _flash_errors(errors)
            return render_template(
                "admin/articles/edit.html",
                article=article,
                data=data,
            ), 400

        update_article(article_id, clean_data)
        flash("Article mis à jour.", "success")
        return redirect(url_for("admin.article_detail", article_id=article_id))

    return render_template("admin/articles/edit.html", article=article)


@bp.route("/articles/<int:article_id>/delete", methods=["POST"])
@admin_required
def article_delete(article_id: int):
    article = get_article_by_id_admin(article_id)

    if article is None:
        abort(404)

    delete_article(article_id)
    flash("Article supprimé.", "info")
    return redirect(url_for("admin.articles_list"))


# =========================
# FORUM
# =========================

@bp.route("/forum", methods=["GET"])
@admin_required
def forum_list():
    """Afficher la liste des sujets du forum côté admin."""
    topics = get_all_topics_for_admin()
    return render_template("admin/forum/list.html", topics=topics)


@bp.route("/forum/<int:topic_id>", methods=["GET"])
@admin_required
def forum_detail(topic_id: int):
    """Afficher le détail d'un sujet du forum côté admin."""
    topic = get_topic_by_id(topic_id)

    if topic is None:
        abort(404)

    replies = get_replies_by_topic_id(topic_id)
    return render_template("admin/forum/detail.html", topic=topic, replies=replies)


@bp.route("/forum/<int:topic_id>/delete", methods=["POST"])
@admin_required
def forum_delete_topic(topic_id: int):
    """Supprimer un sujet du forum côté admin."""
    topic = get_topic_by_id(topic_id)

    if topic is None:
        abort(404)

    delete_topic_by_id(topic_id)
    flash("Sujet supprimé.", "info")
    return redirect(url_for("admin.forum_list"))


@bp.route("/forum/replies/<int:reply_id>/delete", methods=["POST"])
@admin_required
def forum_delete_reply(reply_id: int):
    """Supprimer une réponse du forum côté admin."""
    reply = get_reply_by_id(reply_id)

    if reply is None:
        abort(404)

    topic_id = reply["topic_id"]

    delete_reply_by_id(reply_id)
    flash("Réponse supprimée.", "info")
    return redirect(url_for("admin.forum_detail", topic_id=topic_id))