PRAGMA foreign_keys = ON;

-- =====================================================
-- USERS
-- =====================================================

INSERT INTO user (first_name, last_name, email, password, phone, address, city, role) VALUES
(
    'Mato',
    'NGUAYILA',
    'admin@test.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-54-69-32-58',
    '1 rue du clos dion',
    'Montereau-Fault-Yonne',
    'admin'
),
(
    'Cynthia',
    'DAUVERNE',
    'user@test.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-55-69-32-58',
    '1 rue du clos dion',
    'Montereau-Fault-Yonne',
    'user'
),
(
    'Hakim',
    'BOUDERE',
    'hakim.boudere@gmail.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-56-69-32-58',
    '1 rue de la paix',
    'Paris',
    'user'
),
(
    'Billal',
    'ZEBIR',
    'billal.zerbir@gmail.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-57-69-32-58',
    '1 rue de courcelle',
    'Pantin',
    'user'
),
(
    'Zeyna',
    'SIDIBE',
    'zeyna.sidibe@gmail.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-58-69-32-58',
    '1 rue pasteur',
    'Cachan',
    'user'
),
(
    'Alfred',
    'Macdy',
    'alfred.macdy@gmail.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-59-69-32-58',
    '1 allée de la brume',
    'Evry',
    'user'
),
(
    'Moussa',
    'DIOP',
    'moussa.diop@gmail.com',
    'scrypt:32768:8:1$Mg1qXWVBSM1AbbDh$831a14f3e811cfea8f04ab6b12c13537dae56cbb697b1510d86af86036ec9c335a42d3e3abef3aef51308c3a9ff3373b89e0cf129e87170cb3f35929cfd8caca',
    '07-60-69-32-58',
    '1 rue des champs',
    'Coulommiers',
    'user'
);

-- =====================================================
-- ARTICLES (DEBUT)
-- =====================================================

INSERT INTO articles (name, genres, universe, image, price, release_day) VALUES

-- GOODIES JJK
('Lunette Gojo', 'goodies', 'jujutsu_kaisen', 'image/lunette_gojo.jpg', 57.90, NULL),
('Pendentif Jujutsu Kaisen', 'goodies', 'jujutsu_kaisen', 'image/pendentif_jujutsu_kaisen.jpg', 57.90, NULL),
('Support Gojo Geto', 'goodies', 'jujutsu_kaisen', 'image/support_gojo_geto.jpg', 27.90, NULL),
('Badge Jujutsu Kaisen', 'goodies', 'jujutsu_kaisen', 'image/badge_jujutsu_kaisen.jpg', 27.90, NULL),
('Peruque Itadori', 'goodies', 'jujutsu_kaisen', 'image/peruque_itadori.jpg', 27.90, NULL),
('Book Itadori', 'goodies', 'jujutsu_kaisen', 'image/book_itadori.jpg', 45.90, NULL),

-- DEMON SLAYER
('Lampe Rengoku', 'goodies', 'demon_slayer', 'image/lampe_rengoku.webp', 45.90, NULL),
('Lampe Tanjiro', 'goodies', 'demon_slayer', 'image/lampe_tanjiro.webp', 45.90, NULL),
('Lampe Zenitsu', 'goodies', 'demon_slayer', 'image/lampe_zenitsu.webp', 45.90, NULL),
('Lampe Inosuke', 'goodies', 'demon_slayer', 'image/lampe_inosuke.webp', 45.90, NULL),
('Box Demon Slayer', 'goodies', 'demon_slayer', 'image/box_demon_slayer.jpg', 75.90, NULL),

-- MANGA (EXEMPLE)
('Sekai Saisoku no Isekai Ryokouki','manga',NULL,'image/sekai_saisoku_no_isekai_ryokouki.jpg',7.80,'Lundi'),
('Ordeal','manga',NULL,'image/ordeal.jpg',7.80,'Lundi'),
('Blue Box','manga',NULL,'image/blue_box.jpg',7.80,'Lundi'),
('Dr. Stone','manga',NULL,'image/dr_stone.jpeg',7.90,'Jeudi'),
('One Piece','manga',NULL,'image/one_piece.jpeg',7.90,'Vendredi'),
('Naruto','manga',NULL,'image/naruto.jpeg',7.50,NULL),
('Dragon Ball','manga',NULL,'image/dragon_ball.jpeg',6.90,NULL),

-- FIGURINES
('Figurine Itachi', 'figurine', NULL, 'image/figurine_itachi.jpeg', 52.50, NULL),
('Figurine Naruto', 'figurine', NULL, 'image/figurine_naruto.jpeg', 35.90, NULL),

-- TEXTILE
('Sweat Naruto','textile',NULL,'image/sweat_naruto.jpg',68.50,NULL),
('Veste Luffy','textile',NULL,'image/veste_luffy.jpg',147.90,NULL),

-- VAISSELLE
('Mug Naruto','vaisselle',NULL,'image/mug_naruto.jpg',27.80,NULL),
('Bol Dragon Ball','vaisselle',NULL,'image/bol_dragon_ball.jpg',32.80,NULL)

;
-- =====================================================
-- ORDERS
-- =====================================================

INSERT INTO orders (user_id, total_amount, status) VALUES
(2, 356, 'pending'),
(2, 250, 'paid'),
(3, 425, 'shipped'),
(4, 99, 'delivered'),
(5, 199, 'cancelled');

INSERT INTO orders_articles (order_id, article_id, quantity, unit_price) VALUES
(1, 2, 2, 7.10),
(3, 3, 1, 6.90),
(4, 2, 3, 7.10),
(5, 1, 1, 6.90);

INSERT INTO contact (user_id, sujet, message, status) VALUES
(2, 'Commande', 'Je n''ai toujours pas reçu ma commande', 'answered'),
(3, 'Commande', 'Ma commande est détériorée', 'answered'),
(4, 'Commande', 'Très satisfait', 'read'),
(5, 'Commande', 'Super merci', 'read'),
(6, 'Commande', 'Très bon site', 'pending'),
(7, 'Commande', 'Toujours pas reçu', 'pending');