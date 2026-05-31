from __future__ import annotations

from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.core.security import login_required

from . import bp
from .services import (
    create_reply,
    get_all_topics,
    get_replies_by_topic_id,
    get_topic_by_id,
)
from .services import (
    create_topic as create_topic_service,
)


def _wants_json() -> bool:
    return (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.accept_mimetypes.best == "application/json"
        or request.is_json
    )


def _get_topic_or_404(topic_id: int):
    """Retourne un sujet existant ou déclenche une 404."""
    topic = get_topic_by_id(topic_id)
    if topic is None:
        abort(404)
    return topic


def _topic_payload(topic) -> dict:
    return {
        "id": topic["id"],
        "title": topic["title"],
        "message": topic["message"],
        "excerpt": topic["message"][:180],
        "created_at": topic["created_at"],
        "reply_count": topic["reply_count"],
        "author": {
            "first_name": topic["author_first_name"],
            "last_name": topic["author_last_name"],
            "role": topic["author_role"],
        },
        "url": url_for("forum.topic_detail", topic_id=topic["id"]),
    }


def _reply_payload(reply) -> dict:
    return {
        "id": reply["id"],
        "topic_id": reply["topic_id"],
        "message": reply["message"],
        "created_at": reply["created_at"],
        "author": {
            "first_name": reply["author_first_name"],
            "last_name": reply["author_last_name"],
            "role": reply["author_role"],
        },
    }


@bp.route("/", methods=["GET"])
def index():
    """Afficher la liste des sujets du forum."""
    topics = get_all_topics()
    total_replies = sum(topic["reply_count"] for topic in topics)
    return render_template(
        "forum/index.html",
        topics=topics,
        total_replies=total_replies,
    )


@bp.get("/api/topics")
def api_topics():
    topics = get_all_topics()
    return jsonify(
        {
            "topics": [_topic_payload(topic) for topic in topics],
            "topic_count": len(topics),
            "reply_count": sum(topic["reply_count"] for topic in topics),
        }
    )


@bp.get("/api/topics/<int:topic_id>")
def api_topic(topic_id: int):
    topic = _get_topic_or_404(topic_id)
    replies = get_replies_by_topic_id(topic_id)
    return jsonify(
        {
            "topic": _topic_payload(topic),
            "replies": [_reply_payload(reply) for reply in replies],
            "reply_count": len(replies),
        }
    )


@bp.route("/create", methods=["GET"])
@login_required
def create():
    """Afficher le formulaire de création d'un sujet."""
    return render_template("forum/create.html")


@bp.route("/create", methods=["POST"])
@login_required
def create_topic():
    """Créer un nouveau sujet."""
    if request.is_json:
        payload = request.get_json(silent=True) or {}
        title = str(payload.get("title", "")).strip()
        message = str(payload.get("message", "")).strip()
    else:
        title = request.form.get("title", "").strip()
        message = request.form.get("message", "").strip()

    if not title or not message:
        if _wants_json():
            return jsonify({"error": "Le titre et le message sont obligatoires."}), 400
        flash("Le titre et le message sont obligatoires.", "warning")
        return redirect(url_for("forum.create"))

    topic_id = create_topic_service(
        user_id=session["user_id"],
        title=title,
        message=message,
    )

    if _wants_json():
        topic = get_topic_by_id(topic_id)
        return jsonify({"topic": _topic_payload(topic)}), 201

    flash("Sujet créé avec succès.", "success")
    return redirect(url_for("forum.topic_detail", topic_id=topic_id))


@bp.route("/<int:topic_id>", methods=["GET"])
def topic_detail(topic_id: int):
    """Afficher le détail d'un sujet et ses réponses."""
    topic = _get_topic_or_404(topic_id)
    replies = get_replies_by_topic_id(topic_id)

    return render_template(
        "forum/detail.html",
        topic=topic,
        replies=replies,
    )


@bp.route("/<int:topic_id>/reply", methods=["POST"])
@login_required
def reply(topic_id: int):
    """Ajouter une réponse à un sujet."""
    _get_topic_or_404(topic_id)

    if request.is_json:
        payload = request.get_json(silent=True) or {}
        message = str(payload.get("message", "")).strip()
    else:
        message = request.form.get("message", "").strip()

    if not message:
        if _wants_json():
            return jsonify({"error": "Le message est obligatoire."}), 400
        flash("Le message est obligatoire.", "warning")
        return redirect(url_for("forum.topic_detail", topic_id=topic_id))

    reply_id = create_reply(
        topic_id=topic_id,
        user_id=session["user_id"],
        message=message,
    )

    if _wants_json():
        replies = get_replies_by_topic_id(topic_id)
        created_reply = next(reply for reply in replies if reply["id"] == reply_id)
        return jsonify(
            {
                "reply": _reply_payload(created_reply),
                "replies": [_reply_payload(reply) for reply in replies],
                "reply_count": len(replies),
            }
        ), 201

    flash("Réponse ajoutée avec succès.", "success")
    return redirect(url_for("forum.topic_detail", topic_id=topic_id))
