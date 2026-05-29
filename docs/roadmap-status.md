# Roadmap et état d'avancement — MangaBook V2

Dernière mise à jour : 2026-05-29
Branche de travail actuelle : `feature/design-parity-v1`
Objectif global : refondre `flask-manga-book` en V2 propre, mieux organisée, plus maintenable, tout en conservant le design, le contenu et les fonctionnalités d'origine.

## Méthode de travail

À chaque grosse étape, conserver :

- l'objectif exact ;
- l'état actuel ;
- les fichiers impactés ;
- les risques ;
- les commandes de validation ;
- la preuve visible ;
- la prochaine action exacte.

Avant chaque mise à jour de roadmap, faire un mini-audit repo :

- branche active ;
- diff de branche ;
- fichiers impactés ;
- validation locale disponible ;
- état `git status`.

Commandes de validation de référence :

```bash
python -m compileall app tests
python -m pytest
python -m pytest --cov=app --cov-report=term-missing
ruff check .
ruff format --check .
git status
git diff --stat origin/main...HEAD
```

## Étape 0 — Audit initial V1/V2

### Objectif

Comparer le repo legacy `flask-manga-book` et le repo `flask-manga-book-V2` pour identifier les écarts de structure, conventions, SEO, sécurité, design, contenu et fonctionnalités.

### État

Terminé.

### Constats principaux

- La V2 a une architecture Flask plus propre : application factory, blueprints, services, tests, configuration centralisée.
- Le legacy contient le design et le contenu source à préserver.
- Le legacy contient aussi des données sensibles dans le schéma SQL : ne pas migrer telles quelles.
- La V2 doit encore garantir la parité visuelle et contenu avec la V1.

### Risques identifiés

- Perte du design V1.
- Migration incomplète du contenu.
- Réintroduction de données personnelles ou mots de passe en clair.
- SEO incomplet.
- Validation insuffisante avant merge.

### Preuve

Audit produit dans la conversation et checklist ajoutée dans `docs/parity-checklist.md`.

## Étape 1 — Branche de travail dédiée

### Objectif

Ne pas toucher directement à `main`.

### État

Terminé.

### Branches

```text
audit/parity-legacy-v1
feature/design-parity-v1
```

### Preuve

Les branches distantes existent. `feature/design-parity-v1` est utilisée pour la parité design.

## Étape 2 — SEO public et indexation

### Objectif

Ajouter une base SEO propre sans modifier le design visible.

### Fichiers impactés

- `app/core/seo.py`
- `app/public/routes.py`
- `app/templates/base.html`
- `tests/test_seo.py`

### Ce qui a été fait

- Ajout d'un helper SEO centralisé.
- Ajout de `title`, `description`, `canonical`, `robots`, Open Graph et Twitter Card.
- Ajout de `/robots.txt`.
- Ajout de `/sitemap.xml`.
- Ajout de tests SEO.

### État

Terminé et validé localement.

### Preuve

```text
168 passed
TOTAL 878 statements, 94% coverage
ruff check . -> All checks passed
ruff format --check . -> 34 files already formatted
```

## Étape 3 — Configuration et sécurité runtime

### Objectif

Durcir la configuration Flask sans casser les tests.

### Fichiers impactés

- `app/config.py`
- `.env.example`

### Ce qui a été fait

- `DATABASE` configurable par variable d'environnement.
- `UPLOAD_FOLDER` configurable.
- `MAX_CONTENT_LENGTH` centralisé.
- Cookies HTTPOnly et SameSite activés.
- `SESSION_COOKIE_SECURE` configurable en dev et forcé en production.
- `ProductionConfig` ajoutée.
- Correction : ne plus lire `SECRET_KEY` à l'import, pour éviter de casser pytest.

### État

Terminé et validé localement.

### Preuve

Les tests passent après correction du `KeyError: SECRET_KEY`.

## Étape 4 — Documentation de parité

### Objectif

Conserver une checklist durable pour guider la migration V1 → V2.

### Fichier ajouté

- `docs/parity-checklist.md`

### Contenu

- Parité fonctionnelle.
- Parité contenu.
- Parité design.
- SEO minimum.
- Validation locale obligatoire.
- Critères de fin.

### État

Terminé.

## Étape 5 — Formatage local Ruff

### Objectif

Enregistrer le formatage appliqué localement par Ruff.

### Fichiers impactés

- `app/public/routes.py`
- `tests/test_seo.py`

### État

Terminé et poussé.

### Commit

```text
5dfec2e style: format seo changes
```

### Preuve

```text
On branch audit/parity-legacy-v1
Your branch is up to date with 'origin/audit/parity-legacy-v1'.

nothing to commit, working tree clean
```

## Étape 6 — Parité design V1/V2

### Objectif

Conserver exactement le design d'origine tout en gardant l'architecture propre de la V2.

### État

En cours.

### Mini-audit repo avant mise à jour

Comparaison GitHub :

```text
base: audit/parity-legacy-v1
head: feature/design-parity-v1
status: ahead
ahead_by: 6
behind_by: 0
total_commits: 6
```

Fichiers impactés depuis `audit/parity-legacy-v1` :

```text
app/static/css/public.css          +730
app/static/js/main.js              +276
app/templates/base.html            +132 -30
docs/design-parity-audit.md        +162
docs/design-parity-direct-audit.md +227
```

### Audit design direct

Fichiers documentaires ajoutés :

- `docs/design-parity-audit.md`
- `docs/design-parity-direct-audit.md`

Constats :

- la V2 avait des CSS publics vides ;
- la V2 avait un JS public vide ;
- le layout global V2 était trop simplifié ;
- la V1 contient le header, la recherche, le burger, la nav mobile, le footer, le panier flottant, le popup panier et le scroll-top ;
- la stratégie retenue est de garder routes/services/tests/SEO V2 et de restaurer progressivement les classes/structures visuelles V1.

### Bloc 6A — Shell global public

Objectif : restaurer le socle visuel public commun avant de modifier les pages.

Fichiers impactés :

- `app/templates/base.html`
- `app/static/css/public.css`
- `app/static/js/main.js`

Commits :

```text
216d2ed feat(design): restore public legacy layout shell
214609a feat(design): add public legacy parity styles
91269ba feat(design): restore public legacy interactions
```

Ce qui a été fait :

- header public type V1 ;
- logo/titre Manga Book ;
- recherche globale vers `/articles?q=...` ;
- navigation desktop ;
- navigation mobile ;
- burger menu ;
- dropdown compte ;
- footer ;
- panier flottant ;
- popup panier ;
- bouton scroll-top ;
- CSS public non vide avec classes legacy principales ;
- JS public pour scroll horizontal, burger, dropdown, panier localStorage, popup, scroll-top et flash auto-hide.

Ce qui a été conservé :

- SEO V2 ;
- routes V2 ;
- services V2 ;
- tests V2 ;
- logout en POST ;
- favoris sous forme progressive côté serveur, sans réactiver l'AJAX V1 incompatible.

### Validation locale du bloc 6A

Preuve communiquée :

```text
Fast-forward 1d5448c..91269ba
3 files changed, 1138 insertions(+), 30 deletions(-)
python -m compileall app tests -> OK
python -m pytest -> 168 passed in 123.97s
TOTAL 878 statements, 94% coverage
ruff check . -> All checks passed
ruff format --check . -> 34 files already formatted
git status -> nothing to commit, working tree clean
```

### Risques restants

- Validation visuelle navigateur non encore fournie.
- Les pages `home.html`, `articles.html` et `article_detail.html` restent encore trop éloignées de la V1.
- Certains assets images legacy peuvent manquer côté V2.
- Le panier est localStorage/progressif, pas encore relié à un vrai checkout serveur.

### Prochaine action exacte

Démarrer le bloc 6B : accueil public.

Objectif : adapter `app/public/templates/public/home.html` pour retrouver la structure V1 :

- bannière ;
- intro ;
- sections horizontales ;
- cards legacy ;
- boutons panier ;
- favoris si connecté ;
- compatibilité routes/services V2.

Validation après bloc 6B :

```bash
python -m compileall app tests
python -m pytest
ruff check .
ruff format --check .
git status
```

## Étape 7 — Parité contenu V1/V2

### Objectif

Migrer le contenu utile sans secrets ni données personnelles.

### État

À faire après stabilisation design public prioritaire.

### Actions prévues

1. Extraire les articles publics V1.
2. Nettoyer les données sensibles.
3. Créer des seeds propres.
4. Vérifier images, descriptions, prix, stock, univers, genres, jours de sortie.
5. Ajouter tests ou scripts de vérification.

### Règle stricte

Ne jamais migrer les anciens utilisateurs, emails, téléphones, adresses ou mots de passe réels.

## État global actuel

| Domaine | État |
| --- | --- |
| Branche dédiée | OK |
| Audit initial | OK |
| SEO | OK |
| Robots/sitemap | OK |
| Config sécurité | OK |
| Tests SEO | OK |
| Validation locale | OK : 168 tests, 94% coverage |
| Ruff check | OK |
| Ruff format | OK |
| Documentation parité | OK |
| Formatage local | OK : commit `5dfec2e` poussé |
| Audit design direct | OK |
| Shell global public | OK |
| CSS public legacy minimal | OK |
| JS public legacy minimal | OK |
| Validation bloc design 6A | OK : 168 tests, Ruff OK, git clean |
| Parité accueil | Prochaine étape |
| Parité catalogue | À faire |
| Parité détail article | À faire |
| Parité contenu | À faire |
| PR finale | À faire |

## Prochaine action exacte

Attaquer `home.html` sur la branche `feature/design-parity-v1`.
