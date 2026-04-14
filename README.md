# MangaBook

Application web développée avec **Flask** autour d’un univers manga, conçue avec une architecture modulaire, une séparation claire entre l’espace public et l’espace d’administration, et une base de données initialisée via un schéma SQL dédié.

## Présentation

MangaBook est un projet web full stack centré sur la gestion et la consultation de contenus liés à l’univers manga.  
L’application a été pensée pour structurer plusieurs briques fonctionnelles dans une base technique claire, maintenable et évolutive.

Le projet couvre à la fois des besoins côté utilisateur et côté administration, avec une organisation du code orientée modularité.

## Objectifs du projet

MangaBook a deux objectifs principaux :

### 1. Objectif fonctionnel

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

### 2. Objectif technique

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
- **SQLite** pour l’environnement local actuel
- SQL natif via **`schema.sql`**

### Front-end

- **HTML**
- **CSS / SCSS**
- **JavaScript**

### Outils

- **Git / GitHub**
- **VS Code**
- **venv** pour l’environnement virtuel Python
- **Node.js / npm** uniquement si des outils front sont ajoutés au projet

---

## Principes d’architecture

Le projet repose sur une structure conçue pour rester lisible et scalable :

- **Application Factory** pour l’initialisation de l’application Flask
- **Blueprints séparés** pour les espaces public, admin et modules spécifiques
- **templates isolés par zone fonctionnelle**
- **extensions centralisées**
- **configuration externalisable**
- **base de données initialisée via `schema.sql`**
- **gestion centralisée du contexte applicatif et des erreurs**

Cette organisation permet de réduire le couplage entre les composants, de simplifier la maintenance et de préparer une refonte ou une montée en charge plus propre.

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
│   ├── extensions/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── admin/
│   ├── public/
│   ├── forum/
│   ├── templates/
│   ├── static/
│   └── ...
├── instance/
├── schema.sql
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── package.json   # optionnel si outils front
```
