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

from app.auth.services import get_user_by_id
from app.core.security import login_required

from .services import (
    add_favorite,
    add_to_history,
    create_contact_message,
    get_article_by_id,
    get_featured_articles,
    get_user_favorites,
    get_user_history,
    remove_favorite,
    search_articles,
)

bp = Blueprint(
    "public",
    __name__,
    template_folder="templates",
)


def _get_article_or_404(article_id: int):
    """Retourne un article existant ou déclenche une 404."""
    article = get_article_by_id(article_id)
    if article is None:
        abort(404)
    return article


def _get_current_user_id() -> int | None:
    """Retourne l'identifiant utilisateur courant s'il existe en session."""
    return session.get("user_id")


@bp.route("/")
def home():
    featured_articles = get_featured_articles()
    return render_template("public/home.html", articles=featured_articles)


@bp.route("/articles")
def articles():
    """Afficher le catalogue avec recherche et filtres."""
    filters = {
        "q": request.args.get("q", "").strip(),
        "genre": request.args.get("genre", "").strip(),
        "universe": request.args.get("universe", "").strip(),
        "release_day": request.args.get("release_day", "").strip(),
    }

    articles_list = search_articles(
        query=filters["q"],
        genre=filters["genre"],
        universe=filters["universe"],
        release_day=filters["release_day"],
    )

    return render_template(
        "public/articles.html",
        articles=articles_list,
        filters=filters,
    )


@bp.route("/articles/<int:article_id>")
def article_detail(article_id: int):
    article = _get_article_or_404(article_id)

    user_id = _get_current_user_id()
    if user_id is not None:
        add_to_history(user_id, article_id)

    return render_template("public/article_detail.html", article=article)


# =========================
# PROFIL
# =========================


@bp.route("/profile")
@login_required
def profile():
    """Afficher le profil de l'utilisateur connecté."""
    user = get_user_by_id(session["user_id"])

    if user is None:
        session.clear()
        flash("Session invalide. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("public/profile.html", user=user)


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
    _get_article_or_404(article_id)

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
# SUPPORT / CONTACT
# =========================


@bp.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """Afficher et traiter le formulaire de contact support."""
    if request.method == "POST":
        sujet = request.form.get("sujet", "").strip()
        message = request.form.get("message", "").strip()

        if not sujet or not message:
            flash("Veuillez remplir le sujet et le message.", "warning")
            return redirect(url_for("public.contact"))

        create_contact_message(session["user_id"], sujet, message)
        flash("Votre message a bien été envoyé au support.", "success")
        return redirect(url_for("public.contact"))

    return render_template("public/contact.html")


# =========================
# AUTRES
# =========================


@bp.route("/about")
def about():
    return render_template("public/about.html")
