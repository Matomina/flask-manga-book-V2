# Roadmap MangaBook V2

Cette roadmap est la source de suivi du projet a partir de la migration Python 3.14.

## Etat courant

- Base officielle : `flask-manga-book-V2`.
- Reference visuelle et fonctionnelle : `flask-manga-book` V1.
- Branche de travail actuelle : `feature/python-314-roadmap`.
- Priorite immediate : aligner tout le projet sur Python 3.14 avant la refonte public.

## Checklist globale

### 0. Migration Python 3.14

- [x] Creer une branche dediee.
- [x] Aligner Ruff sur Python 3.14 dans `pyproject.toml`.
- [x] Ajouter `.python-version` avec `3.14`.
- [x] Verifier explicitement Python 3.14 dans la CI.
- [x] Ajouter `python -m compileall app tests` dans la CI.
- [ ] Ouvrir une Pull Request vers `main`.
- [ ] Valider la CI GitHub Actions sur la Pull Request.
- [ ] Merger la Pull Request apres validation.

### 1. Refonte du socle public

- [ ] Creer une branche dediee apres merge de la migration Python 3.14.
- [ ] Corriger `app/templates/base.html`.
- [ ] Eviter de charger `admin.css` sur les pages publiques.
- [ ] Ajouter une base SEO propre dans le layout.
- [ ] Structurer un header public propre et responsive.
- [ ] Ajouter un footer public clair.
- [ ] Valider Ruff, compileall et Pytest.

### 2. Composants UI communs

- [ ] Remplir `app/static/css/components.css`.
- [ ] Creer les styles communs : boutons, cards, badges, forms, flash messages, empty states.
- [ ] Supprimer les styles inline prioritaires.
- [ ] Valider le rendu sur les pages publiques principales.

### 3. CSS public

- [ ] Refaire `app/static/css/public.css` proprement.
- [ ] Reprendre l'identite V1 : violet, rose, fond clair, cartes lumineuses.
- [ ] Stabiliser la grille catalogue.
- [ ] Utiliser `object-fit: contain` pour eviter les images coupees.
- [ ] Valider responsive desktop, tablette et mobile.

### 4. Templates publics

- [ ] Nettoyer `app/public/templates/public/home.html`.
- [ ] Nettoyer `app/public/templates/public/articles.html`.
- [ ] Nettoyer `app/public/templates/public/goodies.html`.
- [ ] Nettoyer `app/public/templates/public/planning.html`.
- [ ] Nettoyer `app/public/templates/public/article_detail.html`.
- [ ] Factoriser ou harmoniser les cartes article.

### 5. SEO et accessibilite

- [ ] Titres de pages clairs.
- [ ] Meta descriptions par page.
- [ ] Alt text images.
- [ ] Hierarchie H1/H2 correcte.
- [ ] Focus visible et navigation clavier.
- [ ] Liens et boutons accessibles.

### 6. Admin roadmap

- [ ] ADMIN-04 : gestion utilisateurs admin.
- [ ] Ajouter la route `/admin/users`.
- [ ] Ajouter la liste utilisateurs.
- [ ] Ajouter le detail utilisateur.
- [ ] Afficher le role et les informations principales.
- [ ] Ajouter les tests admin dedies.

## Commandes de validation standard

```bash
python --version
python -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version"
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

## Regle de validation

Une etape n'est consideree comme terminee que si :

1. les fichiers concernes sont identifies ;
2. les changements sont faits sur une branche dediee ;
3. Ruff, compileall et Pytest passent ;
4. la CI GitHub Actions est verte ;
5. la Pull Request est relue puis mergee ;
6. la roadmap est mise a jour.
