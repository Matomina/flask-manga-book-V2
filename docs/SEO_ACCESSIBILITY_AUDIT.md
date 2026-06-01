# MangaBook V2 — Audit SEO, accessibilité et rendu

## Objectif

Ce document lance la phase 8 de la roadmap : SEO, accessibilité et rendu.

Le but est d'améliorer la qualité HTML, le référencement naturel, l'accessibilité clavier/lecteurs d'écran et les preuves de rendu sans modifier l'identité visuelle déjà validée.

Cette première étape est volontairement audit-only : aucun template, CSS, JavaScript, service, route ou comportement public n'est modifié.

---

## Périmètre audité

Fichiers inspectés :

```text
app/templates/base.html
app/public/templates/public/home.html
app/public/templates/public/articles.html
app/public/templates/public/article_detail.html
app/public/templates/public/goodies.html
app/public/templates/public/planning.html
app/public/templates/public/about.html
app/public/templates/public/legal.html
app/forum/templates/forum/index.html
app/public/routes.py
app/static/css/base.css
```

Pages publiques prioritaires :

```text
/
/articles
/articles/<id>
/goodies
/planning
/about
/mentions-legales
/forum
```

---

## Points déjà solides

### Socle HTML global

Le layout principal définit déjà :

```html
<html lang="fr">
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

Le projet possède aussi un bloc `title`, un bloc `meta_description`, un favicon, une navigation principale, une navigation secondaire et une zone de messages flash avec `role="status"` et `aria-live="polite"`.

### Navigation et structure globale

Points positifs observés :

- navigation principale avec `aria-label="Navigation principale"` ;
- navigation secondaire avec `aria-label="Navigation secondaire"` ;
- bouton burger avec `aria-label`, `aria-controls` et `aria-expanded` ;
- bouton panier flottant avec `aria-label` ;
- popup panier avec `aria-label="Panier"` ;
- focus visible global déjà défini en CSS via `:focus-visible`.

### Images

La majorité des images produit utilisent un `alt` basé sur le nom de l'article. Les bannières principales possèdent déjà des textes alternatifs descriptifs.

### Pages informationnelles

Les pages `about` et `legal` possèdent déjà un `block meta_description`, ce qui constitue une bonne base SEO.

---

## Écarts SEO identifiés

### SEO-01 — Meta descriptions manquantes sur plusieurs pages publiques

Constat : certaines pages utilisent uniquement la meta description générique du layout.

Pages concernées en priorité :

```text
home.html
articles.html
article_detail.html
goodies.html
planning.html
forum/index.html
```

Impact : les pages importantes du site risquent d'avoir une description identique ou trop générique dans les résultats de recherche.

Correction recommandée : ajouter un `block meta_description` spécifique sur chaque page publique prioritaire.

Priorité : P1.

### SEO-02 — Hiérarchie H1/H2 perfectible

Constat : plusieurs pages publiques prioritaires commencent leur contenu principal avec un `<h2>` au lieu d'un `<h1>`.

Pages concernées :

```text
articles.html
goodies.html
planning.html
article_detail.html
about.html
legal.html
```

Le forum possède déjà un `<h1>Forum live</h1>` et l'accueil possède déjà un `<h1>Bienvenue sur MangaBook</h1>`.

Impact : la structure sémantique est moins claire pour les moteurs de recherche et les technologies d'assistance.

Correction recommandée : convertir le titre principal de chaque page en `<h1>` sans changer les classes CSS existantes, afin de préserver le rendu.

Priorité : P1.

### SEO-03 — Titres dynamiques à renforcer sur les détails articles

Constat : la page détail article a déjà un titre dynamique basé sur `article["name"]`, mais pas de meta description dynamique.

Impact : les fiches articles peuvent être moins lisibles dans les résultats de recherche.

Correction recommandée : ajouter une meta description qui combine nom, genre, univers éventuel et disponibilité/stock de manière concise.

Priorité : P2.

### SEO-04 — Absence de canonical ou données structurées

Constat : le layout ne définit pas de lien canonical ni de données structurées JSON-LD.

Impact : ce n'est pas bloquant pour le projet RNCP, mais peut être une amélioration ultérieure.

Correction recommandée : reporter à une phase SEO avancée si le projet doit viser une mise en production réelle.

Priorité : P3.

---

## Écarts accessibilité identifiés

### A11Y-01 — Skip link absent

Constat : le layout ne fournit pas encore de lien d'évitement vers le contenu principal.

Impact : les utilisateurs clavier doivent parcourir toute la navigation avant d'atteindre le contenu.

Correction recommandée : ajouter un lien `.skip-link` vers le contenu principal et donner un `id` au `<main>`.

Priorité : P1.

### A11Y-02 — Landmark main non ciblable

Constat : `<main class="public-main">` n'a pas encore d'identifiant stable.

Impact : impossible d'utiliser un skip link propre vers la zone principale.

Correction recommandée : ajouter `id="contenu-principal"` au `<main>`.

Priorité : P1.

### A11Y-03 — Boutons carrousel avec labels génériques répétés

Constat : plusieurs carrousels utilisent les mêmes libellés `Défiler vers la gauche` et `Défiler vers la droite`.

Impact : en lecture écran, les boutons sont compréhensibles mais peu contextualisés lorsque plusieurs carrousels existent sur la même page.

Correction recommandée : contextualiser progressivement les `aria-label`, par exemple `Défiler les classiques vers la gauche`.

Priorité : P2.

### A11Y-04 — Icône favori parfois non actionnable

Constat : sur la page planning, un article déjà en favori est rendu avec un `<span class="favorite-btn is-favorite" aria-label="Déjà en favori">♥</span>`.

Impact : l'élément a un style de bouton mais n'est pas interactif. Cela peut créer une ambiguïté visuelle et sémantique.

Correction recommandée : soit rendre l'état purement informatif avec une classe dédiée, soit proposer une action cohérente de retrait des favoris.

Priorité : P2.

### A11Y-05 — Liens images et liens texte doublonnés dans les cartes produit

Constat : les cartes ont souvent un lien sur l'image vers le détail et un second lien texte `Voir le détail` vers la même URL.

Impact : ce n'est pas bloquant, mais cela peut allonger la navigation clavier.

Correction recommandée : ne pas modifier immédiatement pour préserver le design, mais envisager une optimisation sémantique plus tard.

Priorité : P3.

---

## Écarts rendu / robustesse identifiés

### UI-01 — Rendu à préserver strictement

Constat : les pages publiques ont été restaurées et validées après les régressions DB/config.

Règle : les corrections Phase 8 doivent éviter tout changement visuel lourd.

Correction recommandée : petites PR séparées, avec validation visuelle locale sur :

```text
/
/articles
/goodies
/planning
/forum
/about
/mentions-legales
```

Priorité : P0.

### UI-02 — Focus visible déjà présent mais skip-link à styliser

Constat : `:focus-visible` existe déjà dans `base.css`.

Correction recommandée : ajouter uniquement une classe `.skip-link` discrète, visible au focus, sans modifier le design courant.

Priorité : P1.

---

## Plan de corrections proposé

### PR 8.2 — Titles, meta descriptions et H1 principaux

Périmètre : templates publics uniquement.

Fichiers probables :

```text
app/public/templates/public/home.html
app/public/templates/public/articles.html
app/public/templates/public/article_detail.html
app/public/templates/public/goodies.html
app/public/templates/public/planning.html
app/forum/templates/forum/index.html
app/public/templates/public/about.html
app/public/templates/public/legal.html
```

Actions :

- ajouter les `block meta_description` manquants ;
- remplacer les titres principaux `<h2>` par `<h1>` en conservant les classes existantes ;
- ne pas modifier les textes ou sections validées hors besoin sémantique.

Validation attendue :

```bash
python -m ruff format --check .
python -m ruff check .
python -m compileall app tests
python -m pytest
git status
git diff --stat
```

### PR 8.3 — Skip link et accessibilité clavier minimale

Périmètre : layout + CSS minimal.

Fichiers probables :

```text
app/templates/base.html
app/static/css/base.css
```

Actions :

- ajouter un skip link ;
- ajouter `id="contenu-principal"` au `<main>` ;
- ajouter une classe CSS `.skip-link` visible au focus seulement.

### PR 8.4 — Smoke tests de structure publique

Périmètre : tests uniquement.

Fichiers probables :

```text
tests/test_public_static_pages.py
tests/test_public.py
```

Actions :

- vérifier présence des H1 sur pages publiques clés ;
- vérifier présence des meta descriptions ;
- vérifier présence du skip link après PR 8.3.

### PR 8.5 — Preuve RNCP SEO/accessibilité

Périmètre : documentation uniquement.

Fichiers probables :

```text
docs/SEO_ACCESSIBILITY_PROOF.md
docs/V2_OPTIMIZATION_ROADMAP.md
```

Actions :

- documenter les corrections effectuées ;
- conserver les preuves de validation ;
- préparer les éléments exploitables dans le dossier RNCP.

---

## Validation de départ Phase 8

Validation locale transmise avant l'audit :

```text
Python 3.14.3
Ruff format : OK
Ruff check : OK
Compileall : OK
Pytest : 232 passed
Coverage : 93%
Git status : nothing to commit, working tree clean
```

---

## Statut

Statut : audit réalisé.

Prochaine action recommandée : ouvrir une PR audit-only, puis traiter PR 8.2 sur les meta descriptions et les H1 principaux.
