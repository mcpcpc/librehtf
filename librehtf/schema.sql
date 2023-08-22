-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS datatype;
DROP TABLE IF EXISTS operator;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS task;

CREATE TABLE datatype (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL
);

INSERT INTO datatype (slug, title) VALUES
        ("str", "string"),
        ("int", "integer"),
        ("float", "floating point");

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

CREATE TABLE device (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        name TEXT UNIQUE NOT NULL,
        description TEXT UNIQUE NOT NULL
);

CREATE TABLE test (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
        name TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        device_id INTEGER NOT NULL,
        FOREIGN KEY(device_id) REFERENCES device(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE task (
        id INTEGER PRIMARY KEY,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT NULL,
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
