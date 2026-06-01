from __future__ import annotations

from pathlib import Path

import pytest


def html(response) -> str:
    return response.get_data(as_text=True)


def test_public_layout_has_skip_link_and_main_target(client):
    response = client.get("/")
    content = html(response)

    assert response.status_code == 200
    assert 'class="skip-link" href="#contenu-principal"' in content
    assert "Aller au contenu principal" in content
    assert 'id="contenu-principal"' in content
    assert 'tabindex="-1"' in content


@pytest.mark.parametrize(
    ("path", "snippet"),
    [
        ("/", "Explorez MangaBook V2"),
        ("/articles", "Parcourez le catalogue MangaBook V2"),
        ("/articles/1", "fiche article, prix, stock"),
        ("/goodies", "Découvrez les goodies MangaBook V2"),
        ("/planning", "Consultez le planning MangaBook V2"),
        ("/forum", "Rejoignez le forum MangaBook V2"),
        ("/a-propos", "Découvrez MangaBook V2"),
        ("/mentions-legales", "Consultez les mentions légales"),
    ],
)
def test_public_pages_have_specific_meta_descriptions(client, path, snippet):
    response = client.get(path)
    content = html(response)

    assert response.status_code == 200
    assert 'name="description"' in content
    assert snippet in content


@pytest.mark.parametrize(
    ("path", "heading"),
    [
        ("/", "Bienvenue sur MangaBook"),
        ("/articles", "Catalogue des articles MangaBook"),
        ("/articles/1", "Solo Leveling Tome 1"),
        ("/goodies", "Goodies MangaBook"),
        ("/planning", "Planning des sorties MangaBook"),
        ("/forum", "Forum live"),
        ("/a-propos", "À propos de MangaBook"),
        ("/mentions-legales", "Mentions légales"),
    ],
)
def test_public_pages_have_h1_structure(client, path, heading):
    response = client.get(path)
    content = html(response)

    assert response.status_code == 200
    assert "<h1" in content
    assert heading in content


def test_skip_link_css_is_defined():
    content = Path("app/static/css/base.css").read_text(encoding="utf-8")

    assert ".skip-link" in content
    assert ".skip-link:focus-visible" in content
    assert "translateY(0)" in content
