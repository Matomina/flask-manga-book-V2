# MangaBook

Application web développée avec **Flask** autour d’un univers manga, pensée avec une architecture modulaire, une séparation claire entre l’espace public et l’espace d’administration, et une base de données initialisée via un schéma SQL dédié.

---

## Présentation

MangaBook est un projet web full stack centré sur la gestion et la consultation de contenus liés à l’univers manga.

L’application a été conçue pour structurer plusieurs briques fonctionnelles dans une base technique claire, maintenable et évolutive. Le projet couvre à la fois des besoins côté utilisateur et côté administration, avec une organisation du code orientée modularité.

---

## Objectifs du projet

MangaBook poursuit deux objectifs principaux.

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

Construire une base de travail propre en appliquant de bonnes pratiques de développement web avec Flask :

- architecture modulaire
- séparation des responsabilités
- configuration centralisée
- base de données structurée
- maintenance facilitée
- évolutivité du projet

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
- **ruff** pour le lint et le formatage

---

## Principes d’architecture

Le projet repose sur une structure conçue pour rester lisible, maintenable et évolutive :

- **Application Factory** pour l’initialisation de l’application Flask
- **Blueprints séparés** pour les espaces public, admin et modules spécifiques
- **templates isolés par zone fonctionnelle**
- **configuration externalisée**
- **extensions centralisées**
- **base de données initialisée via `schema.sql`**
- **gestion centralisée du contexte applicatif et des erreurs**

Cette organisation permet de réduire le couplage entre les composants, de simplifier la maintenance et de préparer la suite du projet sur des bases plus propres.

---

## Fonctionnalités principales

Selon l’état actuel du projet, MangaBook intègre ou prépare les fonctionnalités suivantes :

- authentification utilisateur
- gestion des rôles utilisateur / administrateur
- catalogue d’articles
- détail des articles
- favoris
- historique utilisateur
- gestion des commandes
- formulaire de contact
- forum
- espace d’administration
- tableau de bord administrateur avec statistiques

---

## Structure du projet

Exemple de structure logique du dépôt :

```text
flask-manga-book/
├── manga/
│   ├── __init__.py
│   ├── admin/
│   ├── public/
│   ├── forum/
│   ├── templates/
│   ├── static/
│   └── ...
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
