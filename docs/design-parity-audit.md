# Audit design V1 → V2 — MangaBook

Dernière mise à jour : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Préparer la parité visuelle entre `flask-manga-book` et `flask-manga-book-V2` sans casser l'architecture Flask propre déjà en place.

## État de branche

Branche locale créée : `feature/design-parity-v1`.

État local communiqué :

```text
On branch feature/design-parity-v1
nothing to commit, working tree clean
```

Diff actuel de la branche par rapport à `origin/main` avant changements design :

```text
8 files changed, 737 insertions(+), 17 deletions(-)
```

## Audit local V1 confirmé

Le repo V1 est maintenant disponible localement à côté de la V2.

Templates publics V1 présents :

```text
aide.html
article_detail.html
base.html
catalogue.html
forum.html
forum_detail.html
goodies.html
index.html
panier.html
planning.html
pop-up-panier.html
profil.html
```

Assets publics V1 présents :

```text
css/main.css
css/main.css.map
js/script.js
scss/main.scss
scss/REFACTOR_PLAN.md
scss/abstracts/_mixins.scss
scss/abstracts/_variables.scss
scss/base/_base.scss
scss/base/_index.scss
scss/base/_reset.scss
scss/base/_typography.scss
scss/components/_burger.scss
scss/components/_buttons.scss
scss/components/_cards.scss
scss/components/_dropdown.scss
scss/components/_empty-cart.scss
scss/components/_faq.scss
scss/components/_floating-cart.scss
scss/components/_forms.scss
scss/components/_logo.scss
scss/components/_mobile-nav.scss
scss/components/_scroll-top.scss
scss/components/_scroll.scss
scss/components/_search-bar.scss
scss/layout/_banner.scss
scss/layout/_footer.scss
scss/layout/_header.scss
scss/pages/_aide.scss
scss/pages/_article-detail.scss
scss/pages/_catalogue.scss
scss/pages/_forum.scss
scss/pages/_home.scss
scss/pages/_panier.scss
scss/pages/_planning.scss
scss/pages/_profil.scss
scss/utils/_animations.scss
scss/utils/_breakpoints.scss
```

## Inventaire V2 local confirmé

Templates publics V2 présents :

```text
about.html
articles.html
article_detail.html
contact.html
favorites.html
goodies.html
history.html
home.html
planning.html
profile.html
```

Assets V2 présents :

```text
css/admin.css
css/auth.css
css/base.css
css/components.css
css/forum.css
css/public.css
js/admin.js
js/flash.js
js/main.js
```

## Diagnostic

La V2 a une base Flask et des templates mieux organisés, mais la parité visuelle ne peut pas être considérée comme acquise.

Risque principal : les classes et structures HTML V2 ont été refactorées. Copier directement le SCSS/CSS V1 peut provoquer des styles morts ou des régressions.

Le repo V1 est maintenant disponible localement, donc la suite doit se faire par comparaison de fichiers concrets, pas par supposition.

## Stratégie recommandée

Option hybride :

- garder l'architecture Flask V2 ;
- garder la base admin V2 sauf écart visuel confirmé ;
- restaurer progressivement le design public V1 ;
- réintroduire un pipeline SCSS uniquement si nécessaire ;
- mapper les templates avant modification.

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

Comparer les templates publics prioritaires V1/V2 et commencer par la page d'accueil :

1. `index.html` vers `home.html` ;
2. `catalogue.html` vers `articles.html` ;
3. `article_detail.html` vers `article_detail.html`.

Après chaque correction : lancer `python -m compileall app tests`, `python -m pytest`, `ruff check .`, `ruff format --check .`, puis vérifier `git status`.
