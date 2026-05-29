# Audit design V1 → V2 — MangaBook

Dernière mise à jour : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Préparer la parité visuelle entre `flask-manga-book` et `flask-manga-book-V2` sans casser l'architecture Flask propre déjà en place.

## État de branche

Branche locale créée :

```bash
git checkout -b feature/design-parity-v1
```

État local communiqué :

```text
On branch feature/design-parity-v1
nothing to commit, working tree clean
```

Diff actuel de la branche par rapport à `origin/main` avant changements design :

```text
8 files changed, 737 insertions(+), 17 deletions(-)
```

Fichiers déjà inclus depuis l'étape audit/SEO :

- `.env.example`
- `app/config.py`
- `app/core/seo.py`
- `app/public/routes.py`
- `app/templates/base.html`
- `docs/parity-checklist.md`
- `docs/roadmap-status.md`
- `tests/test_seo.py`

## Audit local V1

Les chemins locaux testés n'existent pas sur le poste :

```powershell
..\flask-manga-book\manga\public\templates
..\flask-manga-book\manga\static\public
```

Erreur observée :

```text
Impossible de trouver le chemin d'accès C:\Users\moi\Documents\Code\flask-manga-book\manga\public\
Impossible de trouver le chemin d'accès C:\Users\moi\Documents\Code\flask-manga-book\manga\static\
```

Conclusion : l'inventaire local V1 ne peut pas être terminé tant que le bon chemin local du repo V1 n'est pas identifié ou tant que le repo V1 n'est pas cloné à côté de la V2.

## Inventaire V2 local confirmé

Templates publics V2 présents :

```text
app/public/templates/public/about.html
app/public/templates/public/articles.html
app/public/templates/public/article_detail.html
app/public/templates/public/contact.html
app/public/templates/public/favorites.html
app/public/templates/public/goodies.html
app/public/templates/public/history.html
app/public/templates/public/home.html
app/public/templates/public/planning.html
app/public/templates/public/profile.html
```

Assets V2 présents :

```text
app/static/css/admin.css
app/static/css/auth.css
app/static/css/base.css
app/static/css/components.css
app/static/css/forum.css
app/static/css/public.css
app/static/js/admin.js
app/static/js/flash.js
app/static/js/main.js
```

## Audit distant V1 via GitHub

Le repo legacy contient des templates publics historiques :

- `manga/public/templates/base.html`
- `manga/public/templates/index.html`
- `manga/public/templates/catalogue.html`
- `manga/public/templates/article_detail.html`
- `manga/public/templates/goodies.html`
- `manga/public/templates/planning.html`
- `manga/public/templates/profil.html`
- `manga/public/templates/panier.html`
- `manga/public/templates/forum.html`
- `manga/public/templates/forum_detail.html`
- `manga/public/templates/aide.html`

Le repo legacy contient aussi un système SCSS public structuré :

- `manga/static/public/scss/main.scss`
- `manga/static/public/scss/abstracts/_variables.scss`
- `manga/static/public/scss/abstracts/_mixins.scss`
- `manga/static/public/scss/base/_reset.scss`
- `manga/static/public/scss/base/_base.scss`
- `manga/static/public/scss/base/_typography.scss`
- `manga/static/public/scss/components/_cards.scss`
- `manga/static/public/scss/components/_buttons.scss`
- `manga/static/public/scss/components/_forms.scss`
- `manga/static/public/scss/components/_burger.scss`
- `manga/static/public/scss/components/_mobile-nav.scss`
- `manga/static/public/scss/components/_search-bar.scss`
- `manga/static/public/scss/components/_floating-cart.scss`
- `manga/static/public/scss/layout/_header.scss`
- `manga/static/public/scss/layout/_footer.scss`
- `manga/static/public/scss/layout/_banner.scss`
- `manga/static/public/scss/pages/_home.scss`
- `manga/static/public/scss/pages/_catalogue.scss`
- `manga/static/public/scss/pages/_article-detail.scss`
- `manga/static/public/scss/pages/_planning.scss`
- `manga/static/public/scss/pages/_profil.scss`
- `manga/static/public/scss/pages/_panier.scss`
- `manga/static/public/scss/pages/_forum.scss`
- `manga/static/public/scss/pages/_aide.scss`
- `manga/static/public/scss/utils/_animations.scss`

JS/CSS legacy notables :

- `manga/static/public/js/script.js`
- `manga/static/admin/admin.js`
- `manga/static/admin/admin.css`
- `package.json`
- `package-lock.json`

## Diagnostic

La V2 a une base Flask et des templates mieux organisés, mais la parité visuelle ne peut pas être considérée comme acquise.

Risque principal : les classes et structures HTML V2 ont été refactorées. Copier directement le SCSS/CSS V1 peut provoquer des styles morts ou des régressions.

## Stratégie recommandée

### Option recommandée : hybride

- Garder l'architecture Flask V2.
- Garder la base admin V2 sauf écart visuel confirmé.
- Restaurer progressivement le design public V1.
- Réintroduire un pipeline SCSS uniquement si nécessaire.
- Mapper les templates avant modification.

## Mapping initial V1 → V2

| V1 | V2 | Priorité | État |
| --- | --- | --- | --- |
| `index.html` | `home.html` | Haute | À comparer |
| `catalogue.html` | `articles.html` | Haute | À comparer |
| `article_detail.html` | `article_detail.html` | Haute | À comparer |
| `goodies.html` | `goodies.html` | Moyenne | À comparer |
| `planning.html` | `planning.html` | Moyenne | À comparer |
| `profil.html` | `profile.html` | Moyenne | À comparer |
| `forum.html` | `forum/index.html` | Moyenne | À comparer |
| `forum_detail.html` | `forum/detail.html` | Moyenne | À comparer |
| `panier.html` | Non confirmé V2 public | Haute si panier requis | À vérifier |
| `aide.html` | `about.html` ou page dédiée | Basse | À arbitrer |

## Prochaine action exacte

Trouver le bon emplacement local du repo V1 ou le cloner à côté de la V2.

Commandes de recherche recommandées :

```powershell
Get-ChildItem C:\Users\moi\Documents\Code -Directory -Recurse -Filter flask-manga-book -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem C:\Users\moi\Documents -Directory -Recurse -Filter flask-manga-book -ErrorAction SilentlyContinue | Select-Object FullName
```

Si le repo V1 n'existe pas localement :

```powershell
cd C:\Users\moi\Documents\Code
git clone https://github.com/Matomina/flask-manga-book.git
cd flask-manga-book-V2
```

Puis relancer :

```powershell
Get-ChildItem ..\flask-manga-book\manga\public\templates -Recurse -File | Select-Object FullName
Get-ChildItem ..\flask-manga-book\manga\static\public -Recurse -File | Select-Object FullName
Get-ChildItem .\app\public\templates -Recurse -File | Select-Object FullName
Get-ChildItem .\app\static -Recurse -File | Select-Object FullName
```
