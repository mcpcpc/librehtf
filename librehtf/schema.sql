-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS task;

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

CREATE TABLE role_permission (
        role_id INTEGER NOT NULL,
        permission_id INTEGER NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        PRIMARY KEY(role_id, permission_id)
        FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
        FOREIGN KEY(permission_id) REFERENCES permission(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        role_id INTEGER NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE,
        FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE device (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL
);

CREATE TABLE test (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        device_id INTEGER NOT NULL,
        FOREIGN KEY(device_id) REFERENCES device(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE task (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        command TEXT NOT NULL,
        test_id INTEGER NOT NULL,
        FOREIGN KEY(test_id) REFERENCES test(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

INSERT INTO role (title, slug) VALUES ("Administrator", "admin"), ("Functional", "functional"), ("Public", "public");
INSERT INTO permission (title, slug) VALUES ("read", "r"), ("update", "rw"), ("insert", "i"), ("delete", "x");
INSERT INTO role_permission (role_id, permission_id) VALUES (1, 1), (1, 2), (1, 3), (1, 4);
INSERT INTO user (role_id, username, password) VALUES (1, "admin", "pbkdf2:sha256:260000$gtvpYNx6qtTuY8rt$2e2a4172758fee088e20d915ac4fdef3bdb07f792e42ecb2a77aa5a72bedd5f5");
