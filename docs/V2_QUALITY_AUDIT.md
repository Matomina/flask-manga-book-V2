\# MangaBook V2 — Audit qualité technique



\## Objectif du document



Ce document formalise l’audit qualité de MangaBook V2 avant les phases de refactoring, sécurisation, nettoyage et préparation du dossier RNCP.



Il sert de base de travail pour mesurer :



\* la qualité du code ;

\* le respect des conventions ;

\* la maintenabilité ;

\* la sécurité ;

\* les tests ;

\* la documentation ;

\* les axes de refactoring ;

\* les preuves techniques exploitables dans le dossier RNCP.



\---



\## État actuel du projet



MangaBook V2 est une application web Flask structurée autour d’une architecture modulaire.



Le projet contient actuellement :



\* une application Flask avec app factory ;

\* des blueprints séparés pour le public, l’authentification, le forum, le panier et l’administration ;

\* des templates Jinja2 organisés par domaine ;

\* des services Python pour isoler une partie de la logique métier ;

\* une base SQLite avec schéma SQL, seed et migrations ;

\* une suite de tests automatisés ;

\* une configuration Ruff ;

\* une CI GitHub Actions ;

\* une documentation projet ;

\* une roadmap d’optimisation dédiée.



\---



\## Fonctionnalités principales déjà présentes



\### Partie publique



\* Page d’accueil.

\* Catalogue d’articles.

\* Recherche et filtres.

\* Tri sécurisé du catalogue.

\* Fiches articles.

\* Goodies.

\* Planning.

\* Favoris.

\* Historique utilisateur.

\* Panier backend synchronisé.

\* Popup panier.

\* Pages à propos, aide et contact regroupées.

\* Pages légales regroupées.



\### Authentification



\* Connexion.

\* Inscription.

\* Déconnexion en POST.

\* Session utilisateur.

\* Gestion des rôles utilisateur/admin.



\### Forum



\* Liste des sujets.

\* Détail des sujets.

\* Création de sujet.

\* Réponses.

\* Endpoints JSON.

\* Interface modernisée.

\* Actions protégées pour les utilisateurs connectés.



\### Administration



\* Dashboard.

\* Gestion des articles.

\* Gestion des utilisateurs.

\* Gestion des commandes.

\* Gestion des contacts.

\* Modération forum.

\* Alertes statistiques.

\* Upload d’images contrôlé.



\---



\## Validation actuelle connue



Dernière validation locale connue :



```text

Python 3.14.3

Ruff format : OK

Ruff check : OK

Compileall : OK

Pytest : 226 passed

Couverture globale : 93%

```



Commandes exécutées :



```bash

python -m ruff format --check .

python -m ruff check .

python -m compileall app tests

python -m pytest

git status

git diff --stat

```



Résultat Git :



```text

nothing to commit, working tree clean

```



\---



\## Points forts techniques



\### Architecture



Le projet utilise une architecture Flask claire avec app factory et blueprints.



Points positifs :



\* séparation des domaines fonctionnels ;

\* organisation lisible ;

\* routes séparées par périmètre ;

\* services métier déjà présents ;

\* templates organisés ;

\* base adaptée pour une montée en complexité.



\### Tests



La suite de tests est solide pour un projet Flask de ce type.



Points positifs :



\* 226 tests automatisés ;

\* couverture globale élevée ;

\* tests routes ;

\* tests services ;

\* tests auth ;

\* tests admin ;

\* tests forum ;

\* tests panier ;

\* tests pages publiques ;

\* validation par CI prévue.



\### Qualité de code



Le projet utilise Ruff pour le formatage et le lint.



Points positifs :



\* conventions Python contrôlées ;

\* imports vérifiés ;

\* erreurs classiques détectées ;

\* style homogène ;

\* base adaptée pour refactoring progressif.



\### Documentation



Le projet dispose déjà de plusieurs documents :



\* README ;

\* roadmap générale ;

\* roadmap de parité fonctionnelle ;

\* roadmap d’optimisation V2.



\---



\## Risques identifiés



\### Risque 1 — Documentation non synchronisée



Certaines documentations peuvent encore indiquer un état ancien du projet, notamment sur le nombre de tests, les étapes terminées ou les prochaines priorités.



Impact :



\* confusion dans le suivi ;

\* preuves RNCP moins solides ;

\* risque de contradiction entre README, roadmaps et état réel.



Action recommandée :



\* synchroniser README et roadmaps après l’audit qualité.



\---



\### Risque 2 — Services admin trop volumineux



Le fichier `app/admin/services.py` concentre plusieurs responsabilités :



\* dashboard ;

\* utilisateurs ;

\* commandes ;

\* contacts ;

\* articles ;

\* validation ;

\* upload.



Impact :



\* maintenabilité réduite ;

\* tests moins ciblés ;

\* évolution plus risquée ;

\* lecture plus difficile pour un évaluateur RNCP.



Action recommandée :



\* découper en services spécialisés.



\---



\### Risque 3 — Configuration sécurité perfectible



La configuration doit être durcie pour éviter les valeurs trop permissives hors environnement de test.



Points à vérifier :



\* `SECRET\_KEY` ;

\* `DEBUG` ;

\* `DATABASE` ;

\* `MAX\_CONTENT\_LENGTH` ;

\* séparation développement/test/production.



Action recommandée :



\* créer une étape de hardening configuration.



\---



\### Risque 4 — Protection CSRF absente ou insuffisante



Les actions POST sensibles doivent être protégées contre les soumissions non autorisées.



Zones concernées :



\* logout ;

\* formulaires admin ;

\* panier ;

\* contact ;

\* forum ;

\* suppression ;

\* changement de statut.



Action recommandée :



\* ajouter une protection CSRF globale et tester les cas critiques.



\---



\### Risque 5 — Migrations panier à renforcer



La table `cart\_items` doit être vérifiée au niveau contraintes SQL et clés étrangères.



Action recommandée :



\* auditer `schema.sql` et `app/db/migrations/\*.sql` ;

\* renforcer ou documenter les choix.



\---



\### Risque 6 — SEO et accessibilité à finaliser



La base HTML est présente, mais un audit final est nécessaire.



Points à contrôler :



\* titres spécifiques ;

\* meta descriptions ;

\* hiérarchie H1/H2 ;

\* textes alternatifs ;

\* navigation clavier ;

\* focus visible ;

\* menu burger ;

\* panier popup ;

\* responsive.



\---



\## Refactoring recommandé



\### 1. Découpage des services admin



Cible :



```text

app/admin/dashboard\_services.py

app/admin/user\_services.py

app/admin/order\_services.py

app/admin/contact\_services.py

app/admin/article\_services.py

app/admin/upload\_services.py

```



Objectif :



\* réduire la taille de `app/admin/services.py` ;

\* clarifier les responsabilités ;

\* faciliter les tests ;

\* améliorer la lisibilité.



\---



\### 2. Centralisation des constantes métier



Certaines constantes métier peuvent être centralisées :



\* genres ;

\* univers ;

\* jours de sortie ;

\* statuts de commande ;

\* extensions upload autorisées.



Objectif :



\* éviter la duplication ;

\* simplifier les validations ;

\* fiabiliser les tests.



\---



\### 3. Renforcement des erreurs métier



Créer des erreurs dédiées lorsque nécessaire :



```text

CartError

RegistrationError

ArticleValidationError

OrderStatusError

UploadValidationError

```



Objectif :



\* rendre les erreurs plus explicites ;

\* éviter les `ValueError` génériques ;

\* améliorer les tests.



\---



\### 4. Nettoyage progressif des templates



Objectif :



\* supprimer les duplications ;

\* harmoniser les composants ;

\* factoriser les cartes articles ;

\* clarifier les formulaires ;

\* améliorer accessibilité et SEO.



\---



\### 5. Nettoyage CSS et JS



Objectif :



\* identifier les fichiers réellement utilisés ;

\* supprimer les anciens styles inutiles ;

\* éviter les doublons ;

\* conserver une structure claire ;

\* documenter les fichiers conservés.



\---



\## Plan de validation recommandé



Pour chaque phase technique :



```bash

python -m ruff format --check .

python -m ruff check .

python -m compileall app tests

python -m pytest

git status

git diff --stat

```



Pour les phases front ou UX :



\* lancer l’application localement ;

\* vérifier les pages principales ;

\* tester desktop/tablette/mobile ;

\* tester les actions utilisateur ;

\* vérifier les formulaires ;

\* vérifier les erreurs ;

\* prendre captures si utile pour RNCP.



Pages à contrôler :



```text

/

&#x20;/articles

&#x20;/goodies

&#x20;/planning

&#x20;/forum/

&#x20;/a-propos

&#x20;/mentions-legales

&#x20;/auth/login

&#x20;/panier

&#x20;/admin/

```



\---



\## Ordre de traitement recommandé



1\. Synchroniser la documentation.

2\. Durcir la configuration.

3\. Refactoriser les services admin.

4\. Ajouter la protection CSRF.

5\. Renforcer DB/migrations.

6\. Finaliser SEO/accessibilité.

7\. Nettoyer fichiers et dossiers inutiles.

8\. Préparer le dossier RNCP.



\---



\## Preuves à conserver pour RNCP



À chaque étape importante, conserver :



\* nom de branche ;

\* capture du `git status` ;

\* résultat `ruff`;

\* résultat `compileall`;

\* résultat `pytest`;

\* couverture de tests ;

\* lien de PR ;

\* résumé des changements ;

\* captures écran si changement visuel ;

\* justification technique ;

\* risques traités.



\---



\## Conclusion



MangaBook V2 dispose déjà d’un socle solide et testable.



La priorité n’est plus de reconstruire le projet, mais de le professionnaliser :



\* documentation synchronisée ;

\* sécurité renforcée ;

\* services mieux découpés ;

\* migrations clarifiées ;

\* SEO/accessibilité finalisés ;

\* nettoyage des fichiers inutiles ;

\* preuves RNCP centralisées.



Cet audit sert de point de départ pour les prochaines branches de stabilisation.



