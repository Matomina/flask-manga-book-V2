# Progression — Bloc 6H Forum public

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Harmoniser les templates forum V2 avec la structure visuelle legacy, sans casser les routes, services et tests forum V2.

## Mini-audit repo

Comparaison depuis le bloc pages privées validé :

```text
base: 5620dde
head: feature/design-parity-v1
status: ahead
ahead_by: 1
behind_by: 0
```

Fichiers impactés :

```text
app/forum/templates/forum/index.html
app/forum/templates/forum/detail.html
app/forum/templates/forum/create.html
app/static/css/public.css
```

## Commit du bloc

```text
e18f7e0 feat: restore legacy forum layout
```

## Ce qui a été fait

- `index.html` : ajout bannière fallback, intro forum, actions, liste de sujets en cards legacy.
- `detail.html` : ajout bannière fallback, retour forum, sujet détaillé, message initial, réponses, formulaire de réponse.
- `create.html` : ajout bannière fallback, section intro et formulaire création sujet en `content`.
- Ajout CSS public pour `topic-card`, `reply-card`, `forum-detail-wrapper`, `forum-message-box`, `reply-form` et `forum-form`.
- Conservation des endpoints V2 : `forum.index`, `forum.create`, `forum.create_topic`, `forum.topic_detail`, `forum.reply`.
- Conservation de `login_required` côté routes pour création et réponse.

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

Bloc 6H validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Les dates forum restent au format actuel fourni par V2.
- Les formulaires forum restent serveur POST, pas AJAX.

## Prochaine action

Faire le point de parité design globale puis attaquer la parité contenu V1 vers V2.
