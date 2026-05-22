CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    active INTEGER DEFAULT 1,

    FOREIGN KEY(role_id) REFERENCES roles(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    serial_number TEXT UNIQUE NOT NULL,
    category_id INTEGER,
    quantity INTEGER DEFAULT 0,
    status TEXT DEFAULT 'available',
    purchase_date TEXT,

    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
    returned_at TEXT,
    active INTEGER DEFAULT 1,

    FOREIGN KEY(material_id) REFERENCES materials(id),
    FOREIGN KEY(employee_id) REFERENCES users(id)
);

CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(material_id) REFERENCES materials(id)
);

CREATE TABLE breakdowns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL,
    reported_by INTEGER NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(material_id) REFERENCES materials(id),
    FOREIGN KEY(reported_by) REFERENCES users(id)
);
