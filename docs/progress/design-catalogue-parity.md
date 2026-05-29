# Progression — Bloc 6C Catalogue public

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Adapter le catalogue public V2 pour retrouver une structure visuelle proche de la V1, tout en conservant les filtres V2.

## Mini-audit repo

Comparaison depuis le bloc accueil valide :

```text
base: 16dd831
head: feature/design-parity-v1
status: ahead
ahead_by: 3
behind_by: 0
```

Fichiers impactés :

```text
app/public/routes.py
app/public/templates/public/articles.html
docs/progress/design-home-parity.md
```

## Commits du bloc

```text
f7a9e4e feat(design): provide favorites for catalogue cards
4570ce9 feat: restore legacy catalogue layout
```

## Ce qui a été fait

- Passage de `favorites_ids` au template catalogue.
- Conservation des filtres V2 : recherche, genre, univers, jour de sortie.
- Remplacement du rendu inline par une structure compatible legacy.
- Ajout du wrapper `catalogue-page`.
- Ajout d'une intro catalogue en section `content`.
- Utilisation de `product-grid`, `product-card`, `card`, `card-info`.
- Ajout des boutons panier compatibles JS localStorage.
- Conservation des liens vers les détails article.

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

Bloc 6C validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Certains textes/accents ont été ajustés localement pour éviter les erreurs de template/formatage.
- Les favoris restent progressifs côté serveur.
- Le panier reste localStorage.

## Prochaine action

Démarrer le bloc 6D : parité détail article `article_detail.html`.
