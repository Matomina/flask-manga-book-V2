from __future__ import annotations


def test_home_page_renders_seo_metadata(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"<title>MangaBook - Catalogue manga et sorties</title>" in response.data
    assert b'<meta name="description"' in response.data
    assert b'<link rel="canonical" href="http://localhost/"' in response.data
    assert b'<meta property="og:title"' in response.data
    assert b'<meta name="twitter:card" content="summary_large_image"' in response.data


def test_article_detail_renders_article_seo_metadata(client):
    response = client.get("/articles/1")

    assert response.status_code == 200
    assert b" - MangaBook</title>" in response.data
    assert b'<link rel="canonical" href="http://localhost/articles/1"' in response.data
    assert b'<meta property="og:title"' in response.data


def test_private_pages_are_noindex(client, auth):
    auth.login_as_user()

    response = client.get("/profile")

    assert response.status_code == 200
    assert b'<meta name="robots" content="noindex, nofollow"' in response.data


def test_robots_txt_exposes_sitemap_and_private_disallows(client):
    response = client.get("/robots.txt")

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert b"User-agent: *" in response.data
    assert b"Disallow: /admin" in response.data
    assert b"Disallow: /auth" in response.data
    assert b"Sitemap: http://localhost/sitemap.xml" in response.data


def test_sitemap_xml_contains_static_and_article_urls(client):
    response = client.get("/sitemap.xml")

    assert response.status_code == 200
    assert response.mimetype == "application/xml"
    assert (
        b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        in response.data
    )
    assert b"<loc>http://localhost/</loc>" in response.data
    assert b"<loc>http://localhost/articles</loc>" in response.data
    assert b"<loc>http://localhost/articles/1</loc>" in response.data
