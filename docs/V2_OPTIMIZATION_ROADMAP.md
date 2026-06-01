# MangaBook V2 — Roadmap optimisation, nettoyage et dossier RNCP

## Objectif

Cette roadmap devient la référence de travail pour terminer proprement MangaBook V2 avant la constitution du dossier RNCP.

Le projet ne repart pas de zéro. La V2 possède déjà une base solide : architecture Flask modulaire, blueprints, services, templates séparés, tests automatisés, Ruff, CI GitHub Actions, pages publiques, panier, forum, authentification, administration et documentation.

L'objectif maintenant est de transformer cette base en version réellement propre, maintenable, sécurisée, documentée et défendable dans un dossier RNCP.

---

## Etat actuel résumé

### Déjà en place

- Application Flask avec app factory.
- Blueprints publics, auth, forum, panier et admin.
- Templates Jinja2 séparés par domaine.
- Services Python dédiés pour une partie de la logique métier.
- Base SQLite avec schéma SQL, seed et migrations.
- Catalogue, détails articles, recherche, tri, planning, goodies.
- Authentification, inscription, profil, favoris, historique.
- Panier backend synchronisé avec le popup public.
- Forum public avec endpoints JSON et interface modernisée.
- Administration : dashboard, articles, utilisateurs, commandes, contacts, forum.
- Pages publiques regroupées : à propos, aide, contact, mentions légales, conditions, confidentialité.
- Ruff, Pytest, coverage et GitHub Actions CI.

### Points de vigilance identifiés

- Corriger en priorité la syntaxe `except TypeError, ValueError` dans `app/admin/services.py`.
- Synchroniser les roadmaps et le README avec l'état réel du projet.
- Durcir la configuration environnement et sécurité.
- Ajouter une protection CSRF sur les formulaires POST sensibles.
- Découper les services admin devenus trop volumineux.
- Renforcer les migrations et contraintes du panier.
- Finaliser SEO, accessibilité, responsive et smoke tests visuels.
- Nettoyer les fichiers, dossiers, styles ou documents devenus inutiles.
- Préparer les preuves RNCP : captures, commandes, tests, CI, PR, architecture, choix techniques.

---

## Règle de travail

Chaque étape doit respecter la méthode suivante :

1. Créer une branche dédiée depuis `main`.
2. Modifier un périmètre limité et clair.
3. Lancer les validations adaptées.
4. Vérifier `git status` et `git diff --stat`.
5. Commit propre avec message explicite.
6. Ouvrir une Pull Request.
7. Attendre CI verte.
8. Merger seulement après validation.
9. Mettre à jour la documentation si nécessaire.

Commandes standard :

```bash
python --version
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

---

## Phase 0 — Figer la roadmap

### Objectif

Sauvegarder dans le repo le plan complet d'optimisation avant de commencer les corrections.

### Branche

```text
docs/v2-optimization-roadmap
```

### Fichier concerné

```text
docs/V2_OPTIMIZATION_ROADMAP.md
```

### Validation attendue

- Le fichier existe dans `docs/`.
- La PR explique clairement le plan.
- Aucun changement fonctionnel n'est inclus dans cette étape.

---

## Phase 1 — Correction bloquante P0

### Objectif

Corriger la syntaxe Python invalide dans `app/admin/services.py`.

### Branche

```text
fix/admin-services-except-syntax
```

### Fichier concerné

```text
app/admin/services.py
```

### Correction attendue

Remplacer :

```python
except TypeError, ValueError:
```

par :

```python
except (TypeError, ValueError):
```

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

### Preuve attendue

- Sortie `compileall` réussie.
- Sortie `pytest` réussie.
- PR dédiée avec CI verte.

---

## Phase 2 — Audit qualité documenté

### Objectif

Créer un document d'audit exploitable pour le projet et réutilisable dans le dossier RNCP.

### Branche

```text
docs/v2-quality-audit
```

### Fichier à créer

```text
docs/V2_QUALITY_AUDIT.md
```

### Contenu attendu

- Objectif de la V2.
- Etat fonctionnel actuel.
- Architecture réelle.
- Qualité de code.
- Conventions.
- Sécurité.
- Tests et CI.
- SEO et accessibilité.
- Dette technique.
- Refactoring recommandé.
- Risques.
- Plan de validation.
- Synthèse utilisable pour RNCP.

### Validation attendue

```bash
git status
git diff --stat
```

---

## Phase 3 — Synchronisation documentation

### Objectif

Mettre à jour les documents existants pour éviter les contradictions entre README, roadmaps et état réel.

### Branche

```text
docs/sync-project-documentation
```

### Fichiers concernés

```text
README.md
docs/ROADMAP.md
docs/functional-parity-roadmap.md
docs/V2_OPTIMIZATION_ROADMAP.md
```

### Corrections attendues

- Actualiser le nombre de tests réel après exécution locale.
- Marquer les étapes fonctionnelles déjà terminées.
- Clarifier les prochaines étapes : qualité, refactor, sécurité, nettoyage, RNCP.
- Harmoniser les noms de fichiers, branches et commandes.

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

---

## Phase 4 — Durcissement configuration et sécurité de base

### Objectif

Rendre la configuration plus professionnelle et moins permissive.

### Branche

```text
hardening/config-security
```

### Fichiers concernés

```text
app/config.py
.env.example
README.md
tests/test_app.py
```

### Corrections attendues

- Ne plus utiliser `SECRET_KEY="dev"` par défaut hors tests.
- Lire `DATABASE` depuis l'environnement quand disponible.
- Désactiver `DEBUG` par défaut.
- Centraliser `MAX_CONTENT_LENGTH` dans la configuration Flask.
- Préserver une configuration de test simple et fiable.

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

---

## Phase 5 — Refactoring admin services

### Objectif

Réduire le fichier admin monolithique et améliorer la séparation des responsabilités.

### Branche

```text
refactor/admin-services-split
```

### Fichiers concernés

```text
app/admin/services.py
app/admin/article_services.py
app/admin/order_services.py
app/admin/user_services.py
app/admin/contact_services.py
app/admin/dashboard_services.py
app/admin/upload_services.py
app/admin/routes.py
tests/test_admin.py
```

### Découpage cible

- `dashboard_services.py` : statistiques dashboard.
- `user_services.py` : liste et détail utilisateurs.
- `order_services.py` : commandes et statuts.
- `contact_services.py` : messages support.
- `article_services.py` : CRUD articles et validation métier.
- `upload_services.py` : upload image et allowlist fichiers.

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

### Preuve attendue

- Tests admin inchangés ou renforcés.
- Aucun changement fonctionnel visible non prévu.
- `git diff --stat` montrant le découpage clair.

---

## Phase 6 — Protection CSRF des actions POST

### Objectif

Protéger les formulaires sensibles contre les soumissions non autorisées.

### Branche

```text
security/add-csrf-protection
```

### Zones concernées

```text
logout
admin articles create/edit/delete
admin orders status
admin contacts delete
admin forum delete/reply
forum create/reply
cart add/update/remove/checkout
contact support
```

### Fichiers probablement concernés

```text
requirements.txt
app/__init__.py
app/templates/base.html
app/admin/templates/admin/base.html
app/public/templates/public/*.html
app/admin/templates/admin/**/*.html
app/forum/templates/forum/*.html
tests/
```

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

### Tests à prévoir

- POST sans token refusé.
- POST avec token accepté.
- JSON/AJAX conservé si nécessaire.
- Logout protégé.
- Admin POST protégés.

---

## Phase 7 — Base de données et migrations

### Objectif

Rendre les migrations plus robustes et cohérentes avec le schéma principal.

### Branche

```text
refactor/db-migrations-hardening
```

### Fichiers concernés

```text
app/db/schema.sql
app/db/connection.py
app/db/migrations/*.sql
tests/test_cart_order_services.py
```

### Points à traiter

- Vérifier les contraintes de `cart_items`.
- Ajouter ou documenter les clés étrangères manquantes.
- Vérifier les index utiles.
- Vérifier les migrations idempotentes.
- Documenter la procédure `flask migrate-db`.

### Validation attendue

```bash
python -m compileall app tests
python -m pytest
```

---

## Phase 8 — SEO, accessibilité et rendu

### Objectif

Améliorer la qualité front sans relancer une refonte design complète.

### Branche

```text
quality/seo-accessibility-polish
```

### Fichiers concernés

```text
app/templates/base.html
app/admin/templates/admin/base.html
app/public/templates/public/*.html
app/forum/templates/forum/*.html
app/static/css/*.css
app/static/js/*.js
```

### Contrôles attendus

- Un seul H1 pertinent par page.
- Titles spécifiques.
- Meta descriptions spécifiques.
- Alt images utiles.
- Focus visible.
- Boutons et liens accessibles au clavier.
- Menu burger utilisable au clavier.
- Panier popup fermable et compréhensible.
- Pages publiques principales responsive.

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

### Smoke test manuel attendu

- `/`
- `/articles`
- `/goodies`
- `/planning`
- `/forum/`
- `/a-propos`
- `/mentions-legales`
- `/auth/login`
- `/panier`
- `/admin/`

---

## Phase 9 — Nettoyage fichiers et dossiers inutiles

### Objectif

Supprimer les éléments devenus inutiles sans casser le projet.

### Branche

```text
chore/cleanup-unused-files
```

### Méthode

Ne supprimer aucun fichier sans preuve.

Pour chaque fichier suspect :

1. Identifier s'il est importé, appelé ou référencé.
2. Vérifier les templates, CSS, JS et tests.
3. Supprimer uniquement si inutilisé.
4. Lancer tests et smoke test.

### Candidats à vérifier

- Anciennes feuilles CSS doublons.
- JS remplacés par une version backend synchronisée.
- Documents roadmap obsolètes ou redondants.
- Images non référencées.
- Templates non utilisés.
- Migrations anciennes non documentées.
- Fichiers générés accidentellement.

### Validation attendue

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

### Preuve attendue

- Liste des fichiers supprimés.
- Justification courte pour chaque suppression.
- CI verte.

---

## Phase 10 — Préparation dossier RNCP

### Objectif

Construire le dossier RNCP à partir d'un projet propre, testé et documenté.

### Branche

```text
docs/rncp-project-evidence
```

### Fichiers à préparer

```text
docs/RNCP_DOSSIER.md
docs/RNCP_ARCHITECTURE.md
docs/RNCP_TESTS_VALIDATION.md
docs/RNCP_SECURITY.md
docs/RNCP_DEPLOYMENT.md
docs/RNCP_SCREENSHOTS.md
```

### Preuves à réunir

- Captures du site public.
- Captures admin.
- Captures forum/panier/auth.
- `pytest` réussi.
- `ruff check` réussi.
- `compileall` réussi.
- CI GitHub Actions verte.
- PRs significatives.
- Schéma architecture.
- Explication sécurité.
- Explication base de données.
- Explication tests.
- Explication choix techniques.

### Validation attendue

```bash
git status
git diff --stat
```

---

## Ordre strict recommandé

1. Phase 0 — Roadmap dans le repo.
2. Phase 1 — Correction syntaxe P0.
3. Phase 2 — Audit qualité documenté.
4. Phase 3 — Synchronisation documentation.
5. Phase 4 — Config et sécurité de base.
6. Phase 5 — Refactoring admin services.
7. Phase 6 — CSRF.
8. Phase 7 — DB/migrations.
9. Phase 8 — SEO/accessibilité/rendu.
10. Phase 9 — Nettoyage fichiers inutiles.
11. Phase 10 — Dossier RNCP.

---

## Statut courant

- [x] Roadmap décidée.
- [x] Document de roadmap ajouté.
- [ ] PR à ouvrir pour figer la roadmap.
- [ ] Phase 1 à démarrer après merge de la roadmap.
