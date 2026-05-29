from __future__ import annotations

from flask import (
    Blueprint,
    Response,
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
from app.core.seo import build_article_description, build_meta

from .services import (
    add_favorite,
    add_to_history,
    create_contact_message,
    get_article_by_id,
    get_articles_grouped_by_release_day,
    get_featured_articles,
    get_goodies_articles,
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


def _article_ids(articles) -> set[int]:
    """Retourner les identifiants d'une liste d'articles sqlite."""
    return {article["id"] for article in articles}


def _get_current_user_favorites_ids() -> set[int]:
    """Retourner les favoris de l'utilisateur courant si connecté."""
    user_id = _get_current_user_id()
    if user_id is None:
        return set()
    return _article_ids(get_user_favorites(user_id))


def _split_featured_articles(articles) -> tuple[list, list]:
    """Séparer les articles mis en avant en sections accueil legacy."""
    midpoint = max(1, len(articles) // 2)
    return articles[:midpoint], articles[midpoint:]


@bp.route("/")
def home():
    featured_articles = get_featured_articles(limit=12)
    classiques, pepites = _split_featured_articles(featured_articles)
    goodies_articles = get_goodies_articles()
    user_id = _get_current_user_id()
    historiques = []
    favorites_ids: set[int] = set()

    if user_id is not None:
        historiques = get_user_history(user_id)
        favorites_ids = _article_ids(get_user_favorites(user_id))

    return render_template(
        "public/home.html",
        articles=featured_articles,
        classiques=classiques,
        pepites=pepites,
        goodies=goodies_articles,
        historiques=historiques,
        favorites_ids=favorites_ids,
        meta=build_meta(
            title="MangaBook - Catalogue manga et sorties",
            description=(
                "Découvrez les nouveautés manga, les sorties planifiées et les "
                "goodies disponibles dans le catalogue MangaBook."
            ),
            canonical=url_for("public.home", _external=True),
        ),
    )


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
        favorites_ids=_get_current_user_favorites_ids(),
        meta=build_meta(
            title="Catalogue manga - MangaBook",
            description=(
                "Parcourez le catalogue MangaBook par recherche, genre, univers "
                "et jour de sortie."
            ),
            canonical=url_for("public.articles", _external=True),
        ),
    )


@bp.route("/articles/<int:article_id>")
def article_detail(article_id: int):
    article = _get_article_or_404(article_id)

    user_id = _get_current_user_id()
    if user_id is not None:
        add_to_history(user_id, article_id)

    article_image = None
    if article["image"]:
        article_image = url_for("static", filename=article["image"], _external=True)

    return render_template(
        "public/article_detail.html",
        article=article,
        meta=build_meta(
            title=f"{article['name']} - MangaBook",
            description=build_article_description(article),
            canonical=url_for(
                "public.article_detail",
                article_id=article_id,
                _external=True,
            ),
            image=article_image,
        ),
    )


# =========================
# GOODIES / PLANNING
# =========================


@bp.route("/goodies")
def goodies():
    """Afficher les articles de type goodies."""
    goodies_articles = get_goodies_articles()
    return render_template(
        "public/goodies.html",
        articles=goodies_articles,
        meta=build_meta(
            title="Goodies manga - MangaBook",
            description=(
                "Retrouvez les goodies manga disponibles dans le catalogue MangaBook."
            ),
            canonical=url_for("public.goodies", _external=True),
        ),
    )


@bp.route("/planning")
def planning():
    """Afficher le planning des sorties par jour."""
    grouped_articles = get_articles_grouped_by_release_day()
    return render_template(
        "public/planning.html",
        grouped_articles=grouped_articles,
        meta=build_meta(
            title="Planning des sorties manga - MangaBook",
            description=(
                "Consultez le planning des sorties MangaBook organisé par jour."
            ),
            canonical=url_for("public.planning", _external=True),
        ),
    )


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

    return render_template(
        "public/profile.html",
        user=user,
        meta=build_meta(
            title="Mon profil - MangaBook",
            description="Consultez les informations de votre compte MangaBook.",
            canonical=url_for("public.profile", _external=True),
            robots="noindex, nofollow",
        ),
    )


# =========================
# FAVORIS
# =========================


@bp.route("/favorites")
@login_required
def favorites():
    user_id = session["user_id"]
    favorite_articles = get_user_favorites(user_id)
    return render_template(
        "public/favorites.html",
        articles=favorite_articles,
        meta=build_meta(
            title="Mes favoris - MangaBook",
            description="Retrouvez vos mangas et goodies favoris sur MangaBook.",
            canonical=url_for("public.favorites", _external=True),
            robots="noindex, nofollow",
        ),
    )


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
    return render_template(
        "public/history.html",
        articles=history_articles,
        meta=build_meta(
            title="Mon historique - MangaBook",
            description="Consultez votre historique de consultation MangaBook.",
            canonical=url_for("public.history", _external=True),
            robots="noindex, nofollow",
        ),
    )


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

    return render_template(
        "public/contact.html",
        meta=build_meta(
            title="Contact - MangaBook",
            description="Contactez le support MangaBook depuis votre espace client.",
            canonical=url_for("public.contact", _external=True),
            robots="noindex, nofollow",
        ),
    )


# =========================
# AUTRES
# =========================


@bp.route("/about")
def about():
    return render_template(
        "public/about.html",
        meta=build_meta(
            title="À propos - MangaBook",
            description=(
                "Découvrez MangaBook, son catalogue manga, ses sorties et ses "
                "fonctionnalités communautaires."
            ),
            canonical=url_for("public.about", _external=True),
        ),
    )


@bp.route("/robots.txt")
def robots_txt():
    """Exposer les règles d'indexation pour les moteurs de recherche."""

    sitemap_url = url_for("public.sitemap_xml", _external=True)
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin",
            "Disallow: /auth",
            "Disallow: /favorites",
            "Disallow: /history",
            "Disallow: /profile",
            f"Sitemap: {sitemap_url}",
            "",
        ]
    )
    return Response(body, mimetype="text/plain")


@bp.route("/sitemap.xml")
def sitemap_xml():
    """Générer un sitemap XML public minimal."""

    articles_list = search_articles()
    static_urls = [
        url_for("public.home", _external=True),
        url_for("public.articles", _external=True),
        url_for("public.goodies", _external=True),
        url_for("public.planning", _external=True),
        url_for("public.about", _external=True),
    ]
    article_urls = [
        url_for("public.article_detail", article_id=article["id"], _external=True)
        for article in articles_list
    ]

    url_items = "\n".join(
        f"  <url><loc>{url}</loc></url>" for url in [*static_urls, *article_urls]
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{url_items}\n"
        "</urlset>\n"
    )

    return Response(body, mimetype="application/xml")
