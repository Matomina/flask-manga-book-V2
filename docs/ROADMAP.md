# Roadmap MangaBook V2

> Statut : roadmap historique.
>
> La roadmap active du projet est désormais `docs/V2_OPTIMIZATION_ROADMAP.md`.
> Cette ancienne roadmap reste conservée comme preuve de suivi projet.

Cette roadmap a servi de source de suivi au moment de la migration Python 3.14 et des premières étapes de structuration de MangaBook V2.

---

## Etat courant

- Base officielle : `flask-manga-book-V2`.
- Reference visuelle et fonctionnelle : `flask-manga-book` V1.
- Branche de travail actuelle : `docs/sync-project-documentation`.
- Priorite immediate : synchroniser la documentation avant hardening, refactoring, nettoyage et dossier RNCP.

---

## Checklist globale historique

### 0. Migration Python 3.14

- [x] Creer une branche dediee.
- [x] Aligner Ruff sur Python 3.14 dans `pyproject.toml`.
- [x] Ajouter `.python-version` avec `3.14`.
- [x] Verifier explicitement Python 3.14 dans la CI.
- [x] Ajouter `python -m compileall app tests` dans la CI.
- [x] Ouvrir une Pull Request vers `main`.
- [x] Valider la CI GitHub Actions sur la Pull Request.
- [x] Merger la Pull Request apres validation.

### 1. Refonte du socle public

- [x] Creer une branche dediee apres merge de la migration Python 3.14.
- [x] Corriger `app/templates/base.html`.
- [x] Eviter de charger `admin.css` sur les pages publiques.
- [x] Ajouter une base SEO propre dans le layout.
- [x] Structurer un header public propre et responsive.
- [x] Ajouter un footer public clair.
- [x] Valider Ruff, compileall et Pytest.

### 2. Composants UI communs

- [x] Remplir `app/static/css/components.css`.
- [x] Creer les styles communs : boutons, cards, badges, forms, flash messages, empty states.
- [x] Supprimer les styles inline prioritaires lorsque c'était nécessaire.
- [x] Valider le rendu sur les pages publiques principales.

### 3. CSS public

- [x] Refaire et enrichir `app/static/css/public.css` progressivement.
- [x] Reprendre l'identite V1 : violet, rose, fond clair, cartes lumineuses.
- [x] Stabiliser la grille catalogue.
- [x] Utiliser des règles d'image adaptées pour éviter les rendus cassés.
- [x] Valider responsive desktop, tablette et mobile.

### 4. Templates publics

- [x] Nettoyer `app/public/templates/public/home.html`.
- [x] Nettoyer `app/public/templates/public/articles.html`.
- [x] Nettoyer `app/public/templates/public/goodies.html`.
- [x] Nettoyer `app/public/templates/public/planning.html`.
- [x] Nettoyer `app/public/templates/public/article_detail.html`.
- [x] Harmoniser les cartes article selon les besoins de parité V1/V2.

### 5. SEO et accessibilite

- [x] Titres de pages clairs dans les templates principaux.
- [x] Meta description de base dans le layout public.
- [x] Alt text images sur les éléments principaux.
- [ ] Audit final H1/H2, focus visible et navigation clavier.
- [ ] Smoke tests finaux SEO/accessibilite avant RNCP.

### 6. Admin roadmap

- [x] ADMIN-04 : gestion utilisateurs admin.
- [x] Ajouter la route `/admin/users`.
- [x] Ajouter la liste utilisateurs.
- [x] Ajouter le detail utilisateur.
- [x] Afficher le role et les informations principales.
- [x] Ajouter les tests admin dedies.

---

## Commandes de validation standard

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

## Etat qualité de référence

Dernière validation locale connue :

```text
Python 3.14.3
Ruff format : OK
Ruff check : OK
Compileall : OK
Pytest : 226 passed
Couverture globale : 93%
```

---

## Regle de validation

Une etape n'est consideree comme terminee que si :

1. les fichiers concernes sont identifies ;
2. les changements sont faits sur une branche dediee ;
3. Ruff, compileall et Pytest passent ;
4. la CI GitHub Actions est verte ;
5. la Pull Request est relue puis mergee ;
6. la documentation est mise a jour si necessaire.

---

## Suite officielle

La suite du projet est désormais suivie dans :

```text
docs/V2_OPTIMIZATION_ROADMAP.md
```

Ordre actif :

1. synchronisation documentation ;
2. hardening configuration et sécurité ;
3. refactoring services admin ;
4. protection CSRF ;
5. renforcement DB/migrations ;
6. SEO/accessibilité/smoke tests ;
7. nettoyage fichiers inutiles ;
8. dossier RNCP.
