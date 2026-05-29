# Audit direct design — V1 vs V2

Date : 2026-05-29
Branche : `feature/design-parity-v1`

## Objectif

Auditer directement les deux repos pour éviter les allers-retours manuels et identifier les corrections prioritaires de parité visuelle.

## Verdict

La V2 est fonctionnelle et mieux organisée côté Flask, mais elle ne conserve pas encore le design public V1.

Le problème principal n'est pas uniquement CSS : la V2 a aussi perdu une grande partie du layout global, des classes HTML legacy et du JavaScript global.

## Écarts critiques

### 1. Layout global

V1 `base.html` contient :

- header `site-header` ;
- logo + titre ;
- menu burger ;
- barre de recherche ;
- navigation desktop ;
- navigation mobile ;
- dropdown utilisateur ;
- footer ;
- panier flottant ;
- popup panier ;
- bouton scroll-top ;
- script global.

V2 `base.html` contient seulement :

- SEO ;
- liens CSS ;
- header simplifié ;
- nav basique ;
- flash messages ;
- block content.

Impact : impossible d'avoir le même design global sans restaurer/adaptater le layout legacy.

### 2. Accueil

V1 `index.html` contient :

- bannière image ;
- wrapper `home-page` ;
- sections `content` ;
- historiques ;
- classiques ;
- pépites ;
- goodies ;
- scroll horizontal ;
- cards legacy ;
- boutons favoris ;
- boutons panier.

V2 `home.html` contient :

- titre simple ;
- lien catalogue ;
- grille inline ;
- articles mis en avant ;
- formulaire contact.

Impact : l'accueil V2 doit être reconstruit autour des blocs legacy tout en gardant les routes/services V2.

### 3. Catalogue

V1 `catalogue.html` contient :

- bannière ;
- wrapper `catalogue-page` ;
- intro ;
- filtres de tri visuels ;
- `product-grid` ;
- `product-card` ;
- `card` ;
- favoris ;
- bouton panier.

V2 `articles.html` contient :

- filtres plus complets et utiles ;
- recherche par query, genre, univers, jour ;
- grille avec styles inline ;
- pas de structure visuelle legacy.

Impact : conserver la logique de filtres V2 mais remplacer le rendu par les classes legacy.

### 4. Détail article

V1 `article_detail.html` contient :

- `content` ;
- `article-detail-wrapper` ;
- `article-detail-image` ;
- bouton favori overlay ;
- `article-detail-info` ;
- `price` ;
- `description` ;
- `article-actions` ;
- bouton panier.

V2 `article_detail.html` contient :

- `article-detail-page` ;
- `article-detail-card` ;
- styles inline ;
- section favoris sous forme de formulaire ;
- pas de bouton panier legacy.

Impact : reprendre les classes V1 en gardant les endpoints favoris V2 et la récupération de description V2.

### 5. CSS public

Les fichiers V2 suivants sont vides :

- `app/static/css/base.css` ;
- `app/static/css/components.css` ;
- `app/static/css/public.css`.

V1 dispose d'un CSS compilé `main.css` et d'une source SCSS complète.

Impact : la V2 ne peut pas être visuellement conforme actuellement.

### 6. JavaScript public

V2 `app/static/js/main.js` est vide.

V1 `script.js` gère :

- scroll horizontal ;
- menu burger ;
- scroll top ;
- formulaires à onglets ;
- panier localStorage ;
- popup panier ;
- favoris AJAX ;
- dropdown utilisateur ;
- FAQ ;
- forum AJAX ;
- auto-hide flash.

Impact : la parité UX demande de restaurer/adaptater le JS legacy.

## Stratégie recommandée

### Phase 1 — Layout global

Adapter `app/templates/base.html` pour restaurer :

- `site-header` ;
- logo/titre ;
- recherche ;
- nav desktop/mobile ;
- footer ;
- panier flottant ;
- popup panier ;
- scroll top ;
- scripts globaux.

Utiliser les endpoints V2 existants.

### Phase 2 — Assets publics

Option rapide : copier le contenu CSS legacy compilé dans `app/static/css/public.css` puis ajuster les chemins/images.

Option propre ensuite : réintroduire SCSS dans `app/static/scss` avec pipeline Sass.

### Phase 3 — JS public

Adapter `script.js` V1 vers `app/static/js/main.js`.

Attention : les endpoints favoris V1 et V2 diffèrent. Le JS favoris doit être adapté pour les routes V2 ou remplacé par des formulaires POST progressifs.

### Phase 4 — Pages prioritaires

Ordre recommandé :

1. `base.html` ;
2. `home.html` ;
3. `articles.html` ;
4. `article_detail.html` ;
5. `goodies.html` ;
6. `planning.html` ;
7. `profile.html` ;
8. forum.

## Décision technique

Ne pas copier aveuglément tous les templates V1.

Conserver :

- routes V2 ;
- services V2 ;
- tests V2 ;
- sécurité V2 ;
- SEO V2.

Restaurer :

- classes HTML legacy ;
- structure visuelle legacy ;
- CSS public legacy ;
- JS public compatible V2.

## Validation obligatoire après chaque bloc

```bash
python -m compileall app tests
python -m pytest
ruff check .
ruff format --check .
git status
```

## Prochaine action exacte

Commencer par `app/templates/base.html`, car c'est le socle commun du rendu V1.

Ne pas modifier l'accueil avant que le layout global et les assets publics soient prêts.
