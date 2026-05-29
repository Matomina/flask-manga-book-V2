# Progression — Bloc 6F Planning public

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Adapter la page planning V2 pour retrouver une structure visuelle proche de la V1, tout en conservant `grouped_articles` V2.

## Mini-audit repo

Comparaison depuis le bloc goodies validé :

```text
base: 6af5090
head: feature/design-parity-v1
status: ahead
ahead_by: 1
behind_by: 0
```

Fichier impacté :

```text
app/public/templates/public/planning.html
```

## Commit du bloc

```text
1041e0b feat: restore legacy planning layout
```

## Ce qui a été fait

- Remplacement du rendu inline V2.
- Ajout d'une bannière fallback.
- Ajout d'une intro legacy en section `content`.
- Conservation des liens catalogue et goodies.
- Conservation des données V2 `grouped_articles`.
- Rendu par jour avec sections `content`.
- Cards en carrousel horizontal via `scroll-container` et `card-list`.
- Boutons panier compatibles JS localStorage.
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

Bloc 6F validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Pas encore d'état favori actif sur la page planning.
- Le panier reste localStorage.

## Prochaine action

Démarrer le bloc 6G : parité profil, favoris et historique.
