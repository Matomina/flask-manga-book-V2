# MangaBook V2

Application web développée avec **Flask** autour d’un univers manga, construite sur une architecture modulaire claire et testée.

Cette version **V2** constitue la **base technique officielle du projet**.  
Elle remplace l’ancien dépôt comme fondation de travail et sert désormais de socle pour la suite du développement, des migrations fonctionnelles et des évolutions visuelles.

---

## Présentation

MangaBook est un projet web full stack centré sur la gestion et la consultation de contenus liés à l’univers manga.

L’objectif de cette V2 est de repartir sur une base plus propre, plus maintenable et plus évolutive que la première version du projet, avec une séparation nette des responsabilités et une architecture Flask structurée.

Le projet couvre à la fois :

- l’espace public
- l’authentification utilisateur
- le forum
- l’administration
- la base de données
- les tests automatisés

---

## Objectifs du projet

### Objectif fonctionnel

Mettre en place une plateforme web permettant de gérer :

- la consultation d’articles manga
- les comptes utilisateurs
- l’authentification
- les favoris
- l’historique utilisateur
- les commandes
- les messages de contact
- le forum avec sujets et réponses
- l’espace d’administration

### Objectif technique

Construire une base de travail sérieuse avec Flask en appliquant de bonnes pratiques :

- architecture modulaire
- séparation claire entre routes, services et logique transverse
- configuration centralisée
- base de données structurée
- tests automatisés
- couverture de code élevée
- maintenance facilitée
- évolutivité du projet

---

## État actuel du projet

Le dépôt V2 est actuellement dans un état **stable et exploitable**.

### Modules déjà structurés

- **auth** : connexion, déconnexion, gestion de session
- **public** : accueil, catalogue, détail article, favoris, historique, contact
- **forum** : liste des sujets, création de sujet, détail, réponses
- **admin** : espace d’administration et gestion métier associée
- **core** : sécurité, filtres, gestion d’erreurs, context processors
- **db** : connexion et initialisation base de données

### Qualité actuelle

- suite de tests automatisés en place
- **81 tests passent**
- **97% de couverture**
- architecture Flask modulaire stabilisée
- base V2 prête pour la suite du projet

---

## Stack technique

### Back-end

- **Python**
- **Flask**
- **Jinja2**
- **SQLite** pour l’environnement local
- SQL natif via **`schema.sql`**

### Front-end

- **HTML**
- **CSS / SCSS**
- **JavaScript**

### Outils

- **Git / GitHub**
- **VS Code**
- **venv** pour l’environnement virtuel Python
- **pytest** pour les tests
- **pytest-cov** pour la couverture
- **ruff** pour le lint

---

## Principes d’architecture

Le projet repose sur une structure pensée pour rester lisible, maintenable et évolutive :

- **Application Factory**
- **Blueprints séparés par domaine fonctionnel**
- **services dédiés à la logique métier**
- **templates organisés par module**
- **configuration centralisée**
- **gestion DB isolée**
- **gestion centralisée des erreurs**
- **outillage de test intégré au projet**

Cette organisation permet de limiter le couplage entre les composants, de mieux isoler les responsabilités, et de faire évoluer l’application plus proprement.

---

## Structure du projet

```text
flask-manga-book-V2/
├── app/
│   ├── __init__.py
│   ├── admin/
│   ├── auth/
│   ├── core/
│   ├── db/
│   ├── forum/
│   ├── public/
│   ├── templates/
│   └── config.py
├── instance/
├── tests/
├── schema.sql
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── .env.example
├── .flaskenv
├── .gitignore
└── run.py
```
