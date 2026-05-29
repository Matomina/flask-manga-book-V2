# Roadmap et état d'avancement — MangaBook V2

Dernière mise à jour : 2026-05-29
Branche de travail : `audit/parity-legacy-v1`
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

### Branche

```bash
audit/parity-legacy-v1
```

### Preuve

La branche distante existe et suit `origin/audit/parity-legacy-v1`.

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

## Étape 5 — Formatage local à pousser

### Objectif

Enregistrer le formatage appliqué localement par Ruff.

### Fichiers modifiés localement

- `app/public/routes.py`
- `tests/test_seo.py`

### État

À terminer côté poste local.

### Commandes à lancer

```bash
git add app/public/routes.py tests/test_seo.py
git commit -m "style: format seo changes"
git push origin audit/parity-legacy-v1
git status
```

### Validation attendue

```text
On branch audit/parity-legacy-v1
Your branch is up to date with 'origin/audit/parity-legacy-v1'.

nothing to commit, working tree clean
```

## Étape 6 — Prochaine grosse étape : parité design V1/V2

### Objectif

Conserver exactement le design d'origine tout en gardant l'architecture propre de la V2.

### Actions prévues

1. Identifier les assets V1 : CSS, SCSS, JS, images, fonts éventuelles.
2. Comparer les templates V1/V2 page par page.
3. Migrer ou adapter les styles dans `app/static/...`.
4. Vérifier les pages : accueil, catalogue, détail article, goodies, planning, profil, favoris, historique, forum, admin.
5. Faire une comparaison desktop/mobile.

### Risques

- Chemins statiques cassés.
- Différences de classes CSS.
- Design admin perturbé.
- Fichiers images manquants.
- Pipeline front incohérent si `package.json` local vient d'un autre projet.

### Validation attendue

```bash
python -m compileall app tests
python -m pytest
ruff check .
ruff format --check .
git diff --stat origin/main...HEAD
```

Validation visuelle attendue : rendu V2 conforme à la V1 sur les pages principales.

## Étape 7 — Prochaine grosse étape : parité contenu V1/V2

### Objectif

Migrer le contenu utile sans secrets ni données personnelles.

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
| Ruff format | OK après formatage local |
| Documentation parité | OK |
| Formatage local | À committer/pusher |
| Parité design | À faire |
| Parité contenu | À faire |
| PR finale | À faire |

## Prochaine action exacte

Sur le poste local :

```bash
git add app/public/routes.py tests/test_seo.py
git commit -m "style: format seo changes"
git push origin audit/parity-legacy-v1
git status
```

Ensuite, démarrer la parité design V1/V2.
