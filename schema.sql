CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE wash_orders (
    id INTEGER PRIMARY KEY,
    address TEXT,
    price INTEGER,
    window_count INTEGER,
    wash_date DATE,
    contact_info TEXT,
    status TEXT, -- 'pending', 'done', 'invoiced', 'paid'
    user_id INTEGER REFERENCES users(id),
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE wash_order_categories (
    wash_order_id INTEGER REFERENCES wash_orders(id),
    category_id INTEGER REFERENCES categories(id),
    UNIQUE(wash_order_id, category_id)
);

CREATE TABLE order_comments (
    id INTEGER PRIMARY KEY,
    wash_order_id INTEGER REFERENCES wash_orders(id),
    user_id INTEGER REFERENCES users(id),
    comment_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO categories (name) VALUES
    ('Kerrostalo'),
    ('Omakotitalo'),
    ('Liiketila'),
    ('Toimistotila'),
    ('Teollisuus');