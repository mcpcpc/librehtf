#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from werkzeug.security import generate_password_hash

from librehtf.db import get_db
from librehtf.auth import token_required

user = Blueprint("user", __name__, url_prefix="/api")


@user.route("/user", methods=("POST",))
@token_required
def create_user():
    """Create user."""

    if not request.form.get("username"):
        return "Username is required.", 400
    elif not request.form.get("password"):
        return "Password is required.", 400
    try:
        db = get_db()
        db.execute(
            "INSERT INTO user (username, password, role_id) VALUES (?, ?, 3)",
            (
                request.form.get("username"),
                generate_password_hash(request.form["password"]),
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "User already exists.", 400
    else:
        return "User successfully created.", 201


@user.route("/user/<int:id>", methods=("GET",))
@token_required
def read_user(id: int):
    """Read user."""

    row = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    if not row:
        return "User does not exist.", 404
    return dict(row)


@user.route("/user/<int:id>", methods=("PUT",))
@token_required
def update_user(id: int):
    """Update user."""

    if not request.form.get("username"):
        return "Username is required.", 400
    elif not request.form.get("password"):
        return "Password is required.", 400
    elif not request.form.get("role_id"):
        return "Role ID is required.", 400
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE user SET username = ?, password = ?, role_id = ? WHERE id = ?",
            (
                request.form.get("username"),
                generate_password_hash(request.form["password"]),
                request.form.get("role_id"),
                id,
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "User already exists.", 400
    else:
        return "User successfully updated.", 201


@user.route("/user/<int:id>", methods=("DELETE",))
@token_required
def delete_user(id: int):
    """Delete user."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return "User successfully deleted.", 200
