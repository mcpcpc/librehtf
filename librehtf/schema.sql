-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS datatype;
DROP TABLE IF EXISTS operator;

CREATE TABLE role (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT NULL,
        active INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        content TEXT DEFAULT NULL
);

INSERT INTO role (slug, title) VALUES
        ("admin", "administrator"),
        ("functional", "functional"),
        ("public", "public");

CREATE TABLE permission (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT NULL,
        active INTEGER NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        content TEXT DEFAULT NULL
);

INSERT INTO permission (slug, title) VALUES
        ("c", "create"),
        ("r", "read"),
        ("u", "update"),
        ("d", "delete");

CREATE TABLE role_permission (
        role_id INTEGER NOT NULL,
        permission_id INTEGER NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        PRIMARY KEY(role_id, permission_id)
        FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
        FOREIGN KEY(permission_id) REFERENCES permission(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO role_permission (role_id, permission_id) VALUES
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (2, 2),
        (3, 2);

CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        role_id INTEGER NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE,
        FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO user (role_id, username, password) VALUES
        (1, "admin", "pbkdf2:sha256:260000$gtvpYNx6qtTuY8rt$2e2a4172758fee088e20d915ac4fdef3bdb07f792e42ecb2a77aa5a72bedd5f5");

CREATE TABLE operator (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL
);

INSERT INTO operator (slug, title) VALUES
        ("none", "unspecified"),
        ("__gt__", "greater than"),
        ("__ge__", "greater than or equal"),
        ("__lt__", "less than"),
        ("__le__", "less than or equal"),
        ("__eq__", "equal"),
        ("__ne__", "not equal");

CREATE TABLE datatype (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL
);

INSERT INTO datatype (slug, title) VALUES
        ("str", "string"),
        ("int", "integer"),
        ("float", "floating point");

CREATE TABLE device (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        description TEXT UNIQUE NOT NULL
);

CREATE TABLE test (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        device_id INTEGER NOT NULL,
        FOREIGN KEY(device_id) REFERENCES device(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE task (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        reference TEXT DEFAULT NULL,
        unit TEXT DEFAULT NULL,
        command TEXT NOT NULL,
        test_id INTEGER NOT NULL,
        operator_id INTEGER NOT NULL,
        datatype_id INTEGER NOT NULL,
        FOREIGN KEY(test_id) REFERENCES test(id) ON DELETE CASCADE ON UPDATE NO ACTION
        FOREIGN KEY(operator_id) REFERENCES operator(id) ON DELETE CASCADE ON UPDATE NO ACTION
        FOREIGN KEY(datatype_id) REFERENCES datatype(id) ON DELETE CASCADE ON UPDATE NO ACTION
);
