# Progression — Bloc 6B Accueil public

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Adapter l'accueil public V2 pour se rapprocher de la structure visuelle V1, sans casser l'architecture Flask V2.

## Mini-audit repo

Comparaison depuis le dernier bloc design validé :

```text
base: 91269ba
head: feature/design-parity-v1
status: ahead
ahead_by: 5
behind_by: 0
```

Fichiers impactés :

```text
app/public/routes.py
app/public/templates/public/home.html
app/static/css/public.css
docs/roadmap-status.md
```

## Commits du bloc

```text
3a06abb feat(design): prepare home legacy sections data
3b784da feat(design): restore legacy home layout
b249922 feat(design): style home fallback visuals
16dd831 style: format home route changes
```

## Ce qui a été fait

- Route `home()` enrichie avec `classiques`, `pepites`, `goodies`, `historiques`, `favorites_ids`.
- Séparation des articles mis en avant en sections accueil.
- Template `home.html` reconstruit avec macros `article_card` et `article_carousel`.
- Ajout d'une bannière fallback.
- Ajout des sections `Historiques`, `Classiques`, `Pépites`, `Goodies`.
- Cards compatibles style legacy.
- Boutons panier compatibles JS localStorage.
- Favoris conservés en formulaire POST serveur.
- Styles fallback pour bannière et images absentes.

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

Bloc 6B validé.

## Risques restants

- Validation visuelle navigateur à faire.
- Assets images legacy à migrer plus tard.
- Panier encore localStorage, pas connecté au checkout serveur.

## Prochaine action

Démarrer le bloc 6C : parité catalogue `articles.html`.
