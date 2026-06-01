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

---

## État qualité

État actuel validé localement :

```text
226 tests passent
Couverture globale : 93%
Ruff format : OK
Ruff check : OK
Compileall : OK
```

Dernière validation complète connue :

```text
tests/test_admin.py                 ✅
tests/test_admin_contact_delete.py  ✅
tests/test_admin_forum_reply.py     ✅
tests/test_app.py                   ✅
tests/test_auth.py                  ✅
tests/test_auth_services.py         ✅
tests/test_cart_json_routes.py      ✅
tests/test_cart_order_services.py   ✅
tests/test_core_filters.py          ✅
tests/test_forum.py                 ✅
tests/test_forum_live.py            ✅
tests/test_public.py                ✅
tests/test_public_services.py       ✅
tests/test_public_static_pages.py   ✅
```

---

## Intégration continue

Le projet utilise une CI GitHub Actions située dans :

```text
.github/workflows/ci.yml
```

La CI se déclenche sur :

- push sur `main` ;
- pull request vers `main`.

Elle exécute automatiquement :

```text
1. installation de Python
2. vérification explicite de Python 3.14
3. installation des dépendances de développement
4. vérification du formatage avec Ruff
5. lint avec Ruff
6. compilation Python avec compileall
7. suite complète Pytest avec couverture
```

---

## Configuration

### `.env.example`

Fichier d’exemple pour les variables d’environnement.

Il contient notamment :

```env
FLASK_ENV=development
FLASK_DEBUG=0
SECRET_KEY=change-me-in-local-env
DATABASE=instance/manga.sqlite
MAX_CONTENT_LENGTH=2097152
TESTING=0
```

### `.flaskenv`

Fichier utilisé pour simplifier le lancement local de Flask :

```env
FLASK_APP=app
FLASK_DEBUG=0
```

### Configuration applicative

La configuration principale est dans :

```text
app/config.py
```

Règles importantes :

- `SECRET_KEY` est obligatoire hors environnement de test ;
- `DEBUG` est désactivé par défaut ;
- `DATABASE` peut être configuré via variable d’environnement ;
- `MAX_CONTENT_LENGTH` est centralisé dans la configuration Flask ;
- les tests utilisent une configuration dédiée avec `SECRET_KEY="test"`.

---

## Sécurité et bonnes pratiques

Le projet applique déjà plusieurs bonnes pratiques :

- session Flask protégée par `SECRET_KEY` ;
- `SECRET_KEY` obligatoire hors environnement de test ;
- `DEBUG` désactivé par défaut ;
- base de données configurable via `DATABASE` ;
- limite d’upload centralisée via `MAX_CONTENT_LENGTH` ;
- accès admin protégé par décorateur ;
- accès utilisateur protégé par décorateur ;
- logout en `POST` ;
- validation serveur des articles ;
- validation des formats d’image ;
- base de données locale ignorée par Git ;
- fichier `.env` ignoré par Git ;
- fichiers générés ignorés par Git ;
- tests automatisés sur les routes, services et protections ;
- CI GitHub Actions pour valider les changements.

Points restants dans la roadmap qualité :

- ajouter une protection CSRF sur les formulaires POST sensibles ;
- renforcer les migrations et contraintes de base de données ;
- documenter les preuves techniques pour le dossier RNCP.

---

## Documentation projet

Documents principaux :

```text
docs/V2_OPTIMIZATION_ROADMAP.md   Roadmap active optimisation / nettoyage / RNCP
docs/V2_QUALITY_AUDIT.md          Audit qualité technique V2
docs/ROADMAP.md                   Roadmap historique conservée comme preuve projet
docs/functional-parity-roadmap.md Roadmap de parité fonctionnelle clôturée
```

---

## Roadmap validée

### Terminé

- Architecture Flask app factory
- Blueprints public, auth, forum, panier, admin
- Base SQLite avec schéma dédié
- Migrations SQL
- Authentification
- Inscription
- Déconnexion POST
- Catalogue public
- Recherche, filtres et tri catalogue
- Fiches articles
- Profil utilisateur
- Favoris
- Historique utilisateur
- Panier backend synchronisé
- Popup panier
- Contact/support public
- Forum public modernisé
- Endpoints JSON forum
- Modération forum admin
- Goodies
- Planning
- Pages à propos / aide / contact regroupées
- Pages légales regroupées
- Dashboard admin enrichi
- Gestion utilisateurs admin
- Gestion commandes admin
- Articles admin renforcés
- Contacts admin améliorés
- Documentation roadmap optimisation
- Audit qualité technique
- Synchronisation documentation
- Configuration de base durcie
- Dépendances production / développement séparées
- Ruff format / lint validé
- Compileall validé
- GitHub Actions CI
- Suite de tests complète

### En cours / prochaines étapes

- Refactoring des services admin
- Protection CSRF des formulaires POST
- Renforcement DB/migrations
- SEO, accessibilité et smoke tests
- Nettoyage fichiers et dossiers inutiles
- Préparation du dossier RNCP

---

## Prochaine étape technique

La prochaine étape technique prévue après le hardening configuration est :

```text
Phase 5 — refactor/admin-services-split
```

Objectifs :

- découper `app/admin/services.py` ;
- créer des services spécialisés admin ;
- conserver les tests admin ;
- valider Ruff, compileall et Pytest.

---

## Auteur

Projet développé par **Matomina** dans le cadre d’une montée en compétence full stack avec Flask, architecture modulaire, tests automatisés et structuration professionnelle de projet.
