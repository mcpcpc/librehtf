#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect
from sqlite3 import PARSE_DECLTYPES
from sqlite3 import Row

from click import command
from click import echo
from flask import current_app
from flask import g


def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """

    if "db" not in g:
        g.db = connect(current_app.config["DATABASE"], detect_types=PARSE_DECLTYPES)
        g.db.row_factory = Row
    return g.db


def close_db(exception=None):
    """
    If this request connected to the database, close the
    connection.
    """

    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""

    db = get_db()
    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))


@command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""

    init_db()
    echo("Initialized the database.")


def init_app(app):
    """
    Register database functions with the Flask app. This is called by
    the application factory.
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
