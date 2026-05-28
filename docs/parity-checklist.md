# Checklist de parité V1 → V2

Objectif : refaire MangaBook avec un code plus propre, tout en conservant le design, le contenu et les fonctionnalités du repo `flask-manga-book`.

## Règles de migration

- Ne jamais travailler directement sur `main`.
- Créer une branche dédiée par sujet : `feature/...`, `fix/...`, `audit/...`.
- Ne pas migrer de données personnelles réelles depuis la V1.
- Ne pas recopier de mot de passe en clair depuis l'ancien `schema.sql`.
- Garder `app/db/schema.sql` pour la structure, et placer les données de démonstration dans des seeds séparés.
- Vérifier chaque étape par tests automatisés ou comparaison visuelle.

## Parité fonctionnelle

| Domaine | Route V2 | Validation attendue | Statut |
| --- | --- | --- | --- |
| Accueil | `/` | rendu 200 + design identique V1 | À vérifier visuellement |
| Catalogue | `/articles` | recherche + filtres + design identique | À vérifier visuellement |
| Détail article | `/articles/<id>` | contenu article + historique connecté | À vérifier visuellement |
| Goodies | `/goodies` | filtre goodies OK | À vérifier |
| Planning | `/planning` | sorties groupées par jour | À vérifier |
| Favoris | `/favorites` | accès connecté + ajout/retrait | Couvert par tests |
| Historique | `/history` | accès connecté | Couvert par tests |
| Profil | `/profile` | accès connecté + session invalide gérée | Couvert par tests |
| Contact | `/contact` | formulaire + validation serveur | Couvert par tests |
| Forum | `/forum` | sujets/réponses/protection | À vérifier |
| Admin dashboard | `/admin` | accès admin + stats | À vérifier |
| Admin articles | `/admin/articles` | CRUD complet + upload image | À vérifier |
| Admin commandes | `/admin/orders` | liste + détail + statut | À vérifier |
| Admin contacts | `/admin/contacts` | lecture + marquage traité | À vérifier |

## Parité contenu

- Extraire les articles V1 sans données personnelles.
- Vérifier pour chaque article :
  - nom ;
  - genre ;
  - univers ;
  - image ;
  - prix ;
  - stock ;
  - jour de sortie ;
  - description publique.
- Copier les images publiques vers `app/static/...` avec chemins compatibles V2.
- Ajouter un seed propre : `app/db/seeds/articles.sql`.

## Parité design

- Comparer les pages V1/V2 dans le navigateur : desktop + mobile.
- Vérifier les assets CSS/JS/images.
- Garder le même rendu visuel : espacements, couleurs, polices, cartes, navigation, responsive.
- Si le SCSS V1 est repris, utiliser un pipeline clair :

```bash
npm install
npm run build:scss
```

## SEO minimum attendu

- `title` par page.
- `meta description` par page.
- `canonical` sur pages publiques.
- `robots noindex` sur pages privées.
- Open Graph + Twitter Card.
- `/robots.txt`.
- `/sitemap.xml`.
- Textes alternatifs sur images dans les templates.

## Validation locale obligatoire

```bash
python -m compileall app tests
python -m pytest
python -m pytest --cov=app --cov-report=term-missing
ruff check .
ruff format --check .
git status
git diff --stat main...HEAD
```

## Critère de fin

La V2 est validable uniquement si :

1. tous les tests passent ;
2. le lint passe ;
3. la comparaison visuelle V1/V2 est conforme ;
4. aucun secret ou donnée personnelle réelle n'est présent ;
5. la PR contient un résumé clair, des preuves de test et les limites restantes.
