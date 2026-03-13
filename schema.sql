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