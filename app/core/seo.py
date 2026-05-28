from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeoMeta:
    """Métadonnées SEO injectées dans les templates publics."""

    title: str = "MangaBook"
    description: str = (
        "MangaBook référence les mangas, sorties, goodies et contenus "
        "associés dans une interface claire et organisée."
    )
    canonical: str | None = None
    image: str | None = None
    robots: str = "index, follow"


def build_meta(
    *,
    title: str = "MangaBook",
    description: str | None = None,
    canonical: str | None = None,
    image: str | None = None,
    robots: str = "index, follow",
) -> SeoMeta:
    """Construire des métadonnées SEO sûres et cohérentes."""

    normalized_description = _truncate_description(
        description
        or (
            "MangaBook référence les mangas, sorties, goodies et contenus "
            "associés dans une interface claire et organisée."
        )
    )

    return SeoMeta(
        title=_normalize_text(title, fallback="MangaBook"),
        description=normalized_description,
        canonical=canonical,
        image=image,
        robots=_normalize_text(robots, fallback="index, follow"),
    )


def build_article_description(article) -> str:
    """Créer une description SEO courte pour une fiche article."""

    raw_description = ""
    if "description" in article.keys() and article["description"]:
        raw_description = article["description"]
    else:
        raw_description = (
            f"{article['name']} est disponible dans le catalogue MangaBook, "
            f"univers {article['universe'] or 'manga'}, genre {article['genres']}."
        )

    return _truncate_description(raw_description)


def _normalize_text(value: str | None, *, fallback: str) -> str:
    normalized = (value or "").strip()
    return normalized or fallback


def _truncate_description(value: str, *, limit: int = 155) -> str:
    normalized = " ".join(value.strip().split())

    if len(normalized) <= limit:
        return normalized

    return normalized[: limit - 1].rstrip() + "…"
