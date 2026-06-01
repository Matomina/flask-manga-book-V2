# MangaBook V2 — Roadmap optimisation, nettoyage et dossier RNCP

## Objectif

Cette roadmap est la référence active pour terminer MangaBook V2 avant la constitution du dossier RNCP.

Le projet possède déjà une base solide : architecture Flask modulaire, blueprints, services, templates séparés, tests automatisés, Ruff, CI GitHub Actions, pages publiques, panier, forum, authentification, administration et documentation.

La suite consiste à professionnaliser le projet : documentation synchronisée, configuration durcie, code mieux découpé, base de données clarifiée, SEO/accessibilité finalisés, nettoyage maîtrisé et preuves RNCP centralisées.

---

## Validation locale de référence

```text
Python 3.14.3
Ruff format : OK
Ruff check : OK
Compileall : OK
Pytest : 232 passed
Coverage : 93%
```

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

## Phases

### Phase 0 — Roadmap dans le repo

Statut : terminé.

- Branche : `docs/v2-optimization-roadmap`.
- Fichier : `docs/V2_OPTIMIZATION_ROADMAP.md`.
- Résultat : roadmap ajoutée puis mergée.

### Phase 1 — Vérification syntaxe P0

Statut : terminé.

- Branche locale : `fix/admin-services-except-syntax`.
- Résultat : aucun correctif nécessaire sur `main`.
- Preuve : Ruff OK, compileall OK, `226 passed`, coverage 93%, working tree clean.

### Phase 2 — Audit qualité documenté

Statut : terminé.

- Branche : `docs/v2-quality-audit`.
- Fichier : `docs/V2_QUALITY_AUDIT.md`.
- Résultat : audit qualité ajouté puis mergé.

### Phase 3 — Synchronisation documentation

Statut : terminé.

- Branche : `docs/sync-project-documentation`.
- Fichiers :

```text
README.md
docs/ROADMAP.md
docs/functional-parity-roadmap.md
docs/V2_OPTIMIZATION_ROADMAP.md
```

Résultat : documentation projet synchronisée, roadmap de parité clôturée et documents d'audit/roadmap centralisés.

### Phase 4 — Configuration projet

Statut : terminé.

- Branche : `hardening/config-security`.
- Fichiers principaux : `app/config.py`, `.env.example`, `README.md`, `tests/test_app.py`.
- Résultat : configuration durcie, `SECRET_KEY` obligatoire hors tests, base locale historique restaurée sur `instance/manga.sqlite`.

### Phase 5 — Refactoring admin

Statut : terminé.

- Branche : `refactor/admin-services-split`.
- Résultat : services admin découpés par responsabilité et tests conservés.

### Phase 6 — Protection des formulaires

Statut : terminé.

- Branche : `csrf-protection`.
- Résultat : protection CSRF centralisée, formulaires POST et requêtes AJAX panier/forum couverts, tests ciblés ajoutés.

### Phase 7 — Base de données et migrations

Statut : terminé.

- Branches :

```text
refactor/db-migrations-hardening-2
refactor/db-schema-alignment
docs/db-hardening-proof
```

- PR réalisées :

```text
PR #26 — restore historical local database path
PR #27 — harden cart item migrations
PR #28 — align db schema with cart constraints
```

- Résultat :
  - base locale historique documentée : `instance/manga.sqlite` ;
  - migrations panier renforcées ;
  - table `cart_items` reconstruite avec contraintes sur bases existantes ;
  - `schema.sql` aligné avec les migrations ;
  - test de structure DB ajouté ;
  - commandes `flask migrate-db` et `flask reset-db` documentées ;
  - preuve RNCP ajoutée dans `docs/DB_HARDENING_PROOF.md`.

- Preuve : Ruff OK, compileall OK, `232 passed`, coverage 93%, working tree clean.

### Phase 8 — SEO, accessibilité et rendu

Statut : à venir.

- Branche prévue : `quality/seo-accessibility-polish`.
- Objectif : finaliser titres, descriptions, H1/H2, alt images, focus visible, navigation clavier, responsive et smoke tests.

### Phase 9 — Nettoyage fichiers inutiles

Statut : à venir.

- Branche prévue : `chore/cleanup-unused-files`.
- Objectif : supprimer uniquement les fichiers prouvés inutiles, avec tests et justification dans la PR.

### Phase 10 — Dossier RNCP

Statut : à venir.

- Branche prévue : `docs/rncp-project-evidence`.
- Objectif : préparer les documents, captures et preuves techniques nécessaires au dossier RNCP.

---

## Ordre strict recommandé

1. Roadmap dans le repo.
2. Vérification syntaxe P0.
3. Audit qualité documenté.
4. Synchronisation documentation.
5. Configuration projet.
6. Refactoring admin.
7. Protection des formulaires.
8. DB/migrations.
9. SEO/accessibilité/rendu.
10. Nettoyage fichiers inutiles.
11. Dossier RNCP.

---

## Statut courant

- [x] Roadmap décidée.
- [x] Document de roadmap ajouté.
- [x] PR roadmap mergée.
- [x] Phase 1 vérifiée : aucun correctif syntaxe nécessaire, `226 passed`.
- [x] Phase 2 réalisée : audit qualité ajouté dans `docs/V2_QUALITY_AUDIT.md`.
- [x] Phase 2 mergée dans `main`.
- [x] Phase 3 terminée : synchronisation documentation.
- [x] Phase 4 terminée : configuration projet durcie.
- [x] Phase 5 terminée : refactoring admin.
- [x] Phase 6 terminée : protection CSRF.
- [x] Phase 7 terminée : DB/migrations stabilisées et preuve ajoutée.
- [ ] Phase 8 à venir : SEO, accessibilité et rendu.
- [ ] Phase 9 à venir : nettoyage fichiers inutiles.
- [ ] Phase 10 à venir : dossier RNCP.
