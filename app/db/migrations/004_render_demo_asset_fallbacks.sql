-- Align demo database image paths with assets committed in the repository.
-- This prevents broken product cards on ephemeral free deployments.

UPDATE articles
SET image = 'image/produit_naruto.jpeg'
WHERE image = 'image/figurine_naruto.jpeg';

UPDATE articles
SET image = 'image/produit_jujutsu_kaisen.jpeg'
WHERE image = 'image/figurine_itachi.jpeg';
