from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.auth.services import get_user_by_id
from app.core.security import login_required

from .favorite_services import toggle_favorite
from .services import (
    add_favorite,
    add_to_history,
    create_contact_message,
    get_article_by_id,
    get_articles_grouped_by_release_day,
    get_goodies_articles,
    get_goodies_sections,
    get_home_sections,
    get_user_favorites,
    get_user_history,
    remove_favorite,
    search_articles,
)

bp = Blueprint("public", __name__, template_folder="templates")


def _get_article_or_404(article_id: int):
    article = get_article_by_id(article_id)
    if article is None:
        abort(404)
    return article


def _get_current_user_id() -> int | None:
    return session.get("user_id")


@bp.route("/")
def home():
    home_sections = get_home_sections(_get_current_user_id())
    return render_template("public/home.html", **home_sections)


@bp.route("/articles")
def articles():
    filters = {
        "q": request.args.get("q", "").strip(),
        "genre": request.args.get("genre", "").strip(),
        "universe": request.args.get("universe", "").strip(),
        "release_day": request.args.get("release_day", "").strip(),
        "sort": request.args.get("sort", "date").strip(),
        "order": request.args.get("order", "desc").strip(),
    }

    articles_list = search_articles(
        query=filters["q"],
        genre=filters["genre"],
        universe=filters["universe"],
        release_day=filters["release_day"],
        sort=filters["sort"],
        order=filters["order"],
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


@bp.route("/goodies")
def goodies():
    goodies_articles = get_goodies_articles()
    goodies_sections = get_goodies_sections()
    return render_template(
        "public/goodies.html",
        articles=goodies_articles,
        goodies_sections=goodies_sections,
    )


@bp.route("/planning")
def planning():
    grouped_articles = get_articles_grouped_by_release_day()
    return render_template("public/planning.html", grouped_articles=grouped_articles)


@bp.route("/profile")
@login_required
def profile():
    user = get_user_by_id(session["user_id"])

    if user is None:
        session.clear()
        flash("Session invalide. Veuillez vous reconnecter.", "warning")
        return redirect(url_for("auth.login"))

    return render_template("public/profile.html", user=user)


@bp.route("/favorites")
@login_required
def favorites():
    favorite_articles = get_user_favorites(session["user_id"])
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


@bp.route("/favorites/toggle/<int:article_id>", methods=["POST"])
@login_required
def toggle_favorite_json(article_id: int):
    _get_article_or_404(article_id)
    status = toggle_favorite(session["user_id"], article_id)
    return jsonify({"status": status})


@bp.route("/history")
@login_required
def history():
    history_articles = get_user_history(session["user_id"])
    return render_template("public/history.html", articles=history_articles)


@bp.route("/cart")
@bp.route("/panier")
@login_required
def cart():
    return redirect(url_for("public_cart.cart"))


@bp.route("/help")
@bp.route("/aide")
def help_page():
    return redirect(url_for("public.about", _anchor="aide"))


@bp.get("/contact")
def contact_page():
    return redirect(url_for("public.about", _anchor="contact"))


@bp.post("/contact")
@login_required
def contact():
    sujet = request.form.get("sujet", "").strip()
    message = request.form.get("message", "").strip()

    if not sujet or not message:
        flash("Veuillez remplir le sujet et le message.", "warning")
        return redirect(url_for("public.about", _anchor="contact"))

    create_contact_message(session["user_id"], sujet, message)
    flash("Votre message a bien été envoyé au support.", "success")
    return redirect(url_for("public.about", _anchor="contact"))


@bp.route("/about")
@bp.route("/a-propos")
def about():
    return render_template("public/about.html")


@bp.route("/mentions-legales")
def legal():
    return render_template("public/legal.html")


@bp.route("/conditions-utilisation")
def terms():
    return redirect(url_for("public.legal", _anchor="conditions-utilisation"))


@bp.route("/politique-confidentialite")
def privacy_policy():
    return redirect(url_for("public.legal", _anchor="politique-confidentialite"))
