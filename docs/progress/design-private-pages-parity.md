# Progression — Bloc 6G Pages privées

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Harmoniser les pages privées V2 avec la structure visuelle legacy, sans casser `login_required`, les routes V2 ni les metas `noindex`.

## Mini-audit repo

Comparaison depuis le bloc planning validé :

```text
base: 0a0e92a
head: feature/design-parity-v1
status: ahead
ahead_by: 1
behind_by: 0
```

Fichiers impactés :

```text
app/public/templates/public/profile.html
app/public/templates/public/favorites.html
app/public/templates/public/history.html
```

## Commit du bloc

```text
e998bd8 feat: restore legacy private pages layout
```

## Ce qui a été fait

- `profile.html` : ajout bannière fallback, `profil-page`, sections `content`, carte infos compte et raccourcis sous forme de cards.
- `favorites.html` : ajout bannière fallback, intro, carrousel de cards, suppression favori en POST, bouton panier localStorage.
- `history.html` : ajout bannière fallback, intro, carrousel de cards et bouton panier localStorage.
- Conservation de l'architecture V2 avec pages séparées.
- Conservation des routes protégées par `login_required`.
- Conservation des metas privées `noindex` côté routes.

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

Bloc 6G validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Le panier reste localStorage.
- Les favoris restent progressifs côté serveur.

## Prochaine action

Démarrer le bloc 6H : parité forum public.
