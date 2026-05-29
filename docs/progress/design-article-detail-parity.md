# Progression — Bloc 6D Détail article

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Adapter la page détail article V2 pour retrouver une structure visuelle proche de la V1, tout en conservant SEO, historique et routes V2.

## Mini-audit repo

Comparaison depuis le bloc catalogue validé :

```text
base: 4570ce9
head: feature/design-parity-v1
status: ahead
ahead_by: 3
behind_by: 0
```

Fichiers impactés :

```text
app/public/routes.py
app/public/templates/public/article_detail.html
docs/progress/design-catalogue-parity.md
```

## Commits du bloc

```text
6faa058 feat(design): provide favorites for article detail
6b92268 feat: restore legacy article detail layout
```

## Ce qui a été fait

- Passage de `favorites_ids` au template détail article.
- Conservation du SEO article V2.
- Conservation de l'ajout à l'historique utilisateur connecté.
- Remplacement de la carte inline V2 par la structure legacy.
- Utilisation de `article-detail-wrapper`.
- Utilisation de `article-detail-image`.
- Utilisation de `article-detail-info`.
- Affichage prix, catégorie, univers, jour de sortie, stock et description.
- Ajout du bouton panier compatible JS localStorage.
- Favoris conservés en formulaires POST serveur.
- Retour catalogue vers `public.articles`.

## Validation locale

```text
python -m compileall app tests -> OK
python -m pytest -> 168 passed
coverage -> 94%
ruff check . -> OK
ruff format --check . -> OK
git status -> clean
```

## Statut

Bloc 6D validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Assets images legacy à vérifier.
- Panier encore localStorage.
- Favoris progressifs serveur, pas AJAX V1.

## Prochaine action

Démarrer le bloc 6E : parité goodies et/ou planning.
