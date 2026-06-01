# MangaBook V2

[![CI](https://github.com/Matomina/flask-manga-book-V2/actions/workflows/ci.yml/badge.svg)](https://github.com/Matomina/flask-manga-book-V2/actions/workflows/ci.yml)

Application web développée avec **Flask**, **Jinja2** et **SQLite**, centrée sur un univers manga, avec catalogue public, forum, espace utilisateur, panier, support/contact et administration.

Le projet a été reconstruit avec une architecture modulaire, une séparation claire entre les blueprints publics, authentification, forum, panier et administration, ainsi qu’une base de tests automatisés solide.

---

## Présentation

MangaBook V2 est un projet full stack orienté web permettant de structurer une plateforme autour de contenus manga et produits dérivés.

L’application permet actuellement de gérer :

- un catalogue d’articles ;
- des fiches articles détaillées ;
- une recherche avec filtres ;
- un tri sécurisé du catalogue ;
- des favoris utilisateurs ;
- un historique de consultation ;
- un profil utilisateur ;
- un panier backend synchronisé avec le popup public ;
- un formulaire de contact/support ;
- un forum public avec sujets, réponses et endpoints JSON ;
- une modération forum côté admin ;
- un dashboard admin enrichi ;
- une gestion admin des articles, utilisateurs, commandes, contacts et forum ;
- des pages publiques complémentaires comme goodies, planning, à propos et mentions légales.

---

## Objectifs du projet

### Objectif fonctionnel

Mettre en place une application web cohérente permettant à un utilisateur de :

- consulter des articles manga ;
- filtrer le catalogue par recherche, genre, univers et jour de sortie ;
- consulter une fiche article ;
- ajouter ou retirer des favoris ;
- gérer un panier ;
- suivre son historique de consultation ;
- accéder à son profil ;
- contacter le support ;
- participer au forum.

Côté administration, l’objectif est de permettre à un administrateur de :

- consulter un dashboard global ;
- gérer les articles ;
- suivre les stocks faibles ou ruptures ;
- consulter les utilisateurs ;
- consulter et mettre à jour les commandes ;
- consulter, filtrer et supprimer les messages de contact ;
- modérer les sujets et réponses du forum.

### Objectif technique

Construire une base Flask propre, maintenable et testée, avec :

- une architecture par blueprints ;
- une app factory Flask ;
- une séparation routes / services / templates ;
- une base SQLite initialisée par schéma SQL ;
- des migrations SQL dédiées ;
- une configuration via variables d’environnement ;
- une suite de tests automatisés ;
- une couverture de code élevée ;
- une configuration qualité avec Ruff, compileall et Pytest ;
- une CI GitHub Actions pour valider automatiquement le projet ;
- une documentation exploitable pour le dossier RNCP.

---

## Stack technique

### Back-end

- Python 3.14
- Flask
- SQLite
- Jinja2
- SQL natif

### Front-end

- HTML
- CSS
- JavaScript progressif
- Jinja2

### Qualité, tests et CI

- Pytest
- Pytest-cov
- Ruff
- Compileall
- GitHub Actions
- Git / GitHub

---

## Architecture du projet

```text
flask-manga-book-V2/
├── .github/workflows/ci.yml
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── admin/
│   ├── auth/
│   ├── core/
│   ├── db/
│   ├── forum/
│   ├── public/
│   ├── static/
│   └── templates/
├── docs/
│   ├── ROADMAP.md
│   ├── functional-parity-roadmap.md
│   ├── V2_OPTIMIZATION_ROADMAP.md
│   └── V2_QUALITY_AUDIT.md
├── tests/
├── .env.example
├── .flaskenv
├── .python-version
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── run.py
└── README.md
```

---

## Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/Matomina/flask-manga-book-V2.git
cd flask-manga-book-V2
```

### 2. Créer et activer l’environnement virtuel

```bash
python -m venv .venv
```

Sous Windows PowerShell :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

Sous macOS / Linux :

```bash
source .venv/bin/activate
```

### 3. Installer les dépendances de développement

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### 4. Préparer le fichier d’environnement

Sous Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

Sous macOS / Linux :

```bash
cp .env.example .env
```

Le fichier `.env` doit contenir une vraie valeur locale pour `SECRET_KEY`.

### 5. Lancer l’application

```bash
flask run
```

Ou :

```bash
python -m flask run
```

Application disponible sur :

```text
http://127.0.0.1:5000
```

---

## Comptes de test

Le projet contient des données de test initialisées via le schéma SQL.

### Administrateur

```text
Email : admin@test.com
Mot de passe : test
```

### Utilisateur

```text
Email : user@test.com
Mot de passe : test
```

---

## Commandes utiles

### Validation complète locale

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

### Lancer les tests

```bash
python -m pytest
```

### Formater le code

```bash
python -m ruff format .
```

### Linter le code

```bash
python -m ruff check .
```

### Appliquer les migrations SQLite

```bash
flask migrate-db
```

Cette commande applique les migrations manquantes sur la base existante sans réinitialiser les données locales.

### Réinitialiser la base SQLite

```bash
flask reset-db
```

Cette commande recrée la base depuis `app/db/schema.sql`, puis réinjecte `app/db/seed.sql`. Elle écrase les données locales existantes de la base configurée dans `DATABASE`.

En développement, la base locale historique du projet est `instance/manga.sqlite`. Ne basculez pas vers une autre base, comme `instance/manga.sqlite3`, sans migration explicite et sauvegarde préalable.
