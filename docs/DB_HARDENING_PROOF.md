# MangaBook V2 — Preuve de durcissement base de données

## Objectif

Ce document centralise les preuves techniques de la phase de durcissement base de données et migrations de MangaBook V2.

Le périmètre était strictement limité à la configuration DB, aux migrations SQLite, au schéma, aux tests et à la documentation. Aucun rendu public, template, CSS, JavaScript public, route publique ou service public n'a été modifié pendant cette phase.

---

## Problèmes identifiés

### 1. Chemin de base locale incohérent

Le projet utilisait deux fichiers SQLite locaux :

```text
instance/manga.sqlite
instance/manga.sqlite3
```

Le changement de configuration avait fait pointer l'application vers `instance/manga.sqlite3`, qui contenait beaucoup moins de données que la base historique.

Diagnostic local observé :

```text
instance/manga.sqlite   -> 507 articles
instance/manga.sqlite3  -> 24 articles
```

Risque corrigé : perte apparente du contenu public local et confusion entre base historique et base nouvellement créée.

### 2. Table `cart_items` insuffisamment contrainte

Audit initial de la table panier :

```sql
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, article_id)
)
```

Contraintes absentes :

```text
CHECK(quantity > 0)
FOREIGN KEY user_id -> user.id ON DELETE CASCADE
FOREIGN KEY article_id -> articles.id ON DELETE CASCADE
idx_cart_items_user_id
idx_cart_items_article_id
```

Risque corrigé : lignes panier incohérentes, quantités invalides, références orphelines et performances de requêtes perfectibles.

### 3. Schéma initial non aligné avec les migrations

Les migrations renforçaient progressivement `cart_items`, mais le schéma de création initiale devait aussi créer directement une table conforme.

Risque corrigé : divergence entre bases neuves et bases migrées.

---

## Actions réalisées

### PR #26 — Correction du chemin de base locale

Objectif : restaurer la base locale historique.

Fichiers concernés :

```text
app/config.py
.env.example
README.md
```

Résultat :

```env
DATABASE=instance/manga.sqlite
```

La documentation rappelle que `instance/manga.sqlite` est la base locale historique du projet.

### PR #27 — Durcissement des migrations panier

Objectif : renforcer `cart_items` pour les bases existantes et les futures migrations.

Fichiers concernés :

```text
app/db/connection.py
app/db/migrations/001_cart.sql
app/db/migrations/003_cart_constraints.sql
```

Résultat :

- migration SQLite spéciale pour reconstruire `cart_items` proprement ;
- conservation des lignes valides existantes ;
- filtrage des lignes invalides ou orphelines ;
- ajout des foreign keys ;
- ajout de `CHECK(quantity > 0)` ;
- ajout des index panier ;
- idempotence conservée via `schema_migrations`.

### PR #28 — Alignement du schéma DB

Objectif : aligner `app/db/schema.sql` avec les migrations panier.

Fichiers concernés :

```text
app/db/schema.sql
tests/test_cart_order_services.py
README.md
```

Résultat :

- `cart_items` est créé directement avec ses contraintes dans `schema.sql` ;
- les bases neuves et les bases migrées ont le même niveau de contraintes ;
- un test vérifie la structure DB de `cart_items` ;
- le README documente `flask migrate-db` et `flask reset-db`.

---

## État final attendu

La table `cart_items` doit contenir :

```text
CHECK(quantity > 0)
FOREIGN KEY user_id -> user.id ON DELETE CASCADE
FOREIGN KEY article_id -> articles.id ON DELETE CASCADE
UNIQUE(user_id, article_id)
idx_cart_items_user_id
idx_cart_items_article_id
```

Les commandes DB sont clarifiées :

```bash
flask migrate-db
```

Applique les migrations manquantes sans réinitialiser les données locales.

```bash
flask reset-db
```

Recrée la base depuis `schema.sql`, réinjecte `seed.sql` et écrase les données locales de la base configurée.

---

## Preuves de validation

Validation locale après la phase DB/schema :

```text
Python 3.14.3
Ruff format : OK
Ruff check : OK
Compileall : OK
Pytest : 232 passed
Coverage : 93%
Git status : nothing to commit, working tree clean
```

Commandes exécutées :

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

---

## Impact RNCP

Cette phase fournit des preuves exploitables pour le dossier RNCP sur :

- l'analyse d'une régression de configuration ;
- la sécurisation de la persistance des données ;
- le renforcement des contraintes SQL ;
- la gestion de migrations SQLite idempotentes ;
- l'ajout de tests automatisés de non-régression ;
- la documentation de procédures sensibles ;
- la validation locale et CI avant merge.

---

## Statut

Statut : terminé.

La phase DB/migrations est considérée stabilisée pour la suite de la roadmap : SEO/accessibilité, nettoyage fichiers inutiles, puis dossier RNCP.
