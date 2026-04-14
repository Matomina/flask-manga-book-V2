# MangaBook

Application web développée avec **Flask** autour d’un univers manga, avec une architecture modulaire, une séparation claire entre l’espace public et l’espace d’administration, et une base de données pilotée par un schéma SQL dédié.

## Objectif du projet

MangaBook est un projet full stack orienté web permettant de structurer une plateforme autour de plusieurs besoins métier :

- consultation d’articles et de contenus manga
- gestion des utilisateurs
- authentification
- favoris et historique
- commandes
- espace d’administration
- messagerie / contact
- forum avec gestion des sujets et réponses

L’objectif technique du projet est aussi de mettre en place une base de travail propre, maintenable et évolutive, en appliquant une architecture Flask sérieuse.

---

## Stack technique

### Back-end

- **Python**
- **Flask**
- **Jinja2**
- **SQLite** pour l’environnement local actuel
- SQL natif via `schema.sql`

### Front-end

- **HTML**
- **CSS / SCSS**
- **JavaScript**

### Outils

- **Git / GitHub**
- **VS Code**
- **venv** pour l’environnement virtuel
- éventuellement **Node.js / npm** si des outils front sont ajoutés au projet

---

## Principes d’architecture

Le projet repose sur une organisation pensée pour être claire et scalable :

- **Application Factory** pour l’initialisation de l’application Flask
- **Blueports séparés** pour les zones publiques et admin
- **templates isolés par module**
- **extensions centralisées**
- **configuration externalisable**
- **base SQL initialisée via `schema.sql`**
- **gestion des erreurs et du contexte au niveau app**

Cette approche permet de limiter le couplage, de rendre la maintenance plus simple, et de préparer une évolution plus propre du projet.

---

## Fonctionnalités principales

Selon l’état actuel du projet, MangaBook intègre ou prépare les fonctionnalités suivantes :

- authentification utilisateur
- gestion des rôles utilisateur / administrateur
- catalogue d’articles
- détail d’articles
- favoris
- historique utilisateur
- gestion des commandes
- formulaire de contact
- forum
- espace d’administration
- tableau de bord admin avec statistiques

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
├── package.json
└── .gitignore
```
