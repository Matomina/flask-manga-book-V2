# Déploiement gratuit - MangaBook V2

Ce document prépare un déploiement gratuit de démonstration pour MangaBook V2.

## Option recommandée

Render est l’option la plus simple pour exposer rapidement cette application Flask avec un serveur WSGI.

La configuration automatisée est fournie dans `render.yaml`.

## Limite importante avec SQLite

La configuration gratuite utilise :

```text
DATABASE=/tmp/manga.sqlite
```

Cette base est adaptée à une démonstration, mais elle n’est pas persistante durablement. Les données peuvent être perdues lors d’un redémarrage, d’un redeploy ou d’un changement d’instance.

Pour une vraie production, il faudra migrer vers PostgreSQL ou utiliser un stockage persistant compatible.

## Variables d’environnement prévues

`SECRET_KEY` doit être créée manuellement dans l’interface de l’hébergeur.

Ne jamais la committer dans Git.

Exemple de génération locale :

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Variables prévues :

```text
SECRET_KEY=<valeur-secrete-a-creer-dans-l-hebergeur>
FLASK_ENV=production
FLASK_DEBUG=0
DATABASE=/tmp/manga.sqlite
MAX_CONTENT_LENGTH=2097152
AUTO_SEED_DEMO=1
```

## Initialisation automatique de démonstration

`AUTO_SEED_DEMO=1` active une initialisation contrôlée au démarrage :

1. Si le schéma de base n’existe pas, l’application exécute `schema.sql` puis les migrations.
2. Si la table `articles` est vide, l’application injecte `seed.sql`.
3. Les migrations sont relancées après l’injection pour aligner la base.

Cette option est prévue pour un hébergement gratuit de démonstration avec SQLite temporaire.

Elle ne doit pas remplacer une stratégie de base de données de production.

## Commandes de déploiement

Build command :

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

Start command :

```bash
gunicorn "run:app"
```

## Validation locale avant déploiement

Depuis la racine du repo :

```bash
python -m pip install -r requirements.txt
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
```

Test de démarrage WSGI local :

```bash
gunicorn "run:app"
```

Sous Windows, Gunicorn ne s’exécute pas nativement. Le test complet doit être fait sur Linux, WSL, CI ou l’hébergeur.
