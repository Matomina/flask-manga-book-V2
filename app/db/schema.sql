PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS contact;
DROP TABLE IF EXISTS orders_articles;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS detail_articles_public;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK (trim(first_name) <> ''),
    last_name TEXT NOT NULL CHECK (trim(last_name) <> ''),
    email TEXT NOT NULL UNIQUE CHECK (trim(email) <> ''),
    password TEXT NOT NULL CHECK (trim(password) <> ''),
    phone TEXT UNIQUE,
    address TEXT,
    city TEXT,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_role ON user(role);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (trim(name) <> ''),
    genres TEXT NOT NULL CHECK (
        genres IN ('manga', 'figurine', 'textile', 'vaisselle', 'goodies')
    ),
    universe TEXT CHECK (
        universe IS NULL OR universe IN (
            'naruto',
            'jujutsu_kaisen',
            'one_piece',
            'demon_slayer',
            'dragon_ball'
        )
    ),
    image TEXT NOT NULL CHECK (trim(image) <> ''),
    price REAL NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL DEFAULT 10 CHECK (stock >= 0),
    release_day TEXT CHECK (
        release_day IS NULL OR release_day IN (
            'Lundi',
            'Mardi',
            'Mercredi',
            'Jeudi',
            'Vendredi',
            'Samedi',
            'Dimanche',
            'Sans jour fixe'
        )
    ),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_articles_genres ON articles(genres);
CREATE INDEX idx_articles_universe ON articles(universe);
CREATE INDEX idx_articles_release_day ON articles(release_day);
CREATE INDEX idx_articles_created_at ON articles(created_at);

CREATE TABLE detail_articles_public (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL UNIQUE,
    description TEXT NOT NULL CHECK (trim(description) <> ''),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    UNIQUE (user_id, article_id)
);

CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    UNIQUE (user_id, article_id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    status TEXT NOT NULL CHECK (
        status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')
    ),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE orders_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE RESTRICT,
    UNIQUE (order_id, article_id)
);

CREATE TABLE contact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    sujet TEXT NOT NULL CHECK (trim(sujet) <> ''),
    message TEXT NOT NULL CHECK (trim(message) <> ''),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (
        status IN ('pending', 'read', 'answered')
    ),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
);

CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL CHECK (trim(title) <> ''),
    message TEXT NOT NULL CHECK (trim(message) <> ''),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL CHECK (trim(message) <> ''),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_detail_articles_public_article_id
    ON detail_articles_public(article_id);

CREATE INDEX idx_history_user_id ON history(user_id);
CREATE INDEX idx_history_article_id ON history(article_id);
CREATE INDEX idx_history_viewed_at ON history(viewed_at);

CREATE INDEX idx_favorites_user_id ON favorites(user_id);
CREATE INDEX idx_favorites_article_id ON favorites(article_id);
CREATE INDEX idx_favorites_created_at ON favorites(created_at);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);

CREATE INDEX idx_orders_articles_order_id ON orders_articles(order_id);
CREATE INDEX idx_orders_articles_article_id ON orders_articles(article_id);

CREATE INDEX idx_contact_user_id ON contact(user_id);
CREATE INDEX idx_contact_status ON contact(status);
CREATE INDEX idx_contact_created_at ON contact(created_at);

CREATE INDEX idx_topics_user_id ON topics(user_id);
CREATE INDEX idx_topics_created_at ON topics(created_at);

CREATE INDEX idx_replies_topic_id ON replies(topic_id);
CREATE INDEX idx_replies_user_id ON replies(user_id);
CREATE INDEX idx_replies_created_at ON replies(created_at);