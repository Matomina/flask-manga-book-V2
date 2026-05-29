# Progression — Bloc 6E Goodies public

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Adapter la page goodies V2 pour retrouver une structure visuelle proche de la V1, tout en conservant la route V2.

## Mini-audit repo

Comparaison depuis le bloc détail article validé :

```text
base: a44e6a1
head: feature/design-parity-v1
status: ahead
ahead_by: 1
behind_by: 0
```

Fichier impacté :

```text
app/public/templates/public/goodies.html
```

## Commit du bloc

```text
0f1cc71 feat: restore legacy goodies layout
```

## Ce qui a été fait

- Remplacement du rendu inline V2.
- Ajout d'une bannière fallback.
- Ajout d'une intro legacy en section `content`.
- Conservation des liens catalogue et planning.
- Rendu des goodies avec `product-grid`, `product-card`, `card`, `card-info`.
- Ajout des boutons panier compatibles JS localStorage.
- Favoris conservés en formulaires POST serveur.
- Gestion des images absentes avec `card-placeholder`.

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

Bloc 6E validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Les sections V1 par univers/catégorie ne sont pas encore reconstituées car la route V2 fournit une liste plate.
- Le panier reste localStorage.
- Les favoris restent progressifs côté serveur.

## Prochaine action

Démarrer le bloc 6F : parité planning public `planning.html`.
