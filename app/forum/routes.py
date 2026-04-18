from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.core.security import login_required
from .services import (
    create_reply,
    create_topic as create_topic_service,
    get_all_topics,
    get_replies_by_topic_id,
    get_topic_by_id,
)

bp = Blueprint(
    "forum",
    __name__,
    url_prefix="/forum",
    template_folder="templates",
)


def _get_topic_or_404(topic_id: int):
    """Retourne un sujet existant ou déclenche une 404."""
    topic = get_topic_by_id(topic_id)
    if topic is None:
        abort(404)
    return topic


@bp.route("/", methods=["GET"])
def index():
    topics = get_all_topics()
    return render_template("forum/index.html", topics=topics)


@bp.route("/create", methods=["POST"])
@login_required
def create_topic():
    title = request.form.get("title", "").strip()
    message = request.form.get("message", "").strip()

    if not title or not message:
        flash("Le titre et le message sont obligatoires.", "warning")
        return redirect(url_for("forum.index"))

    topic_id = create_topic_service(
        user_id=session["user_id"],
        title=title,
        message=message,
    )

    flash("Sujet créé avec succès.", "success")
    return redirect(url_for("forum.topic_detail", topic_id=topic_id))


@bp.route("/<int:topic_id>", methods=["GET"])
def topic_detail(topic_id: int):
    topic = _get_topic_or_404(topic_id)
    replies = get_replies_by_topic_id(topic_id)
    return render_template(
        "forum/topic_detail.html",
        topic=topic,
        replies=replies,
    )


@bp.route("/<int:topic_id>/reply", methods=["POST"])
@login_required
def reply(topic_id: int):
    _get_topic_or_404(topic_id)

    message = request.form.get("message", "").strip()

    if not message:
        flash("Le message est obligatoire.", "warning")
        return redirect(url_for("forum.topic_detail", topic_id=topic_id))

    create_reply(
        topic_id=topic_id,
        user_id=session["user_id"],
        message=message,
    )

    flash("Réponse ajoutée avec succès.", "success")
    return redirect(url_for("forum.topic_detail", topic_id=topic_id))