#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from werkzeug.security import generate_password_hash

from librehtf.db import get_db
from librehtf.token import token_required

user = Blueprint("user", __name__, url_prefix="/api")


@user.post("/user")
@token_required
def create_user():
    """Create user."""

    form = request.form.copy().to_dict()
    form["password"] = generate_password_hash(form["password"])
    try:
        db = get_db()
        db.execute(
            """
            INSERT INTO user (
                username,
                password,
                role_id
            ) VALUES (
                :username,
                :password,
                3
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "User successfully created.", 201


@user.get("/user/<int:id>")
@token_required
def read_user(id: int):
    """Read user."""

    row = get_db().execute(
        "SELECT * FROM user WHERE id = ?",
        (id,),
    ).fetchone()
    if not row:
        return "User does not exist.", 404
    return dict(row)


@user.put("/user/<int:id>")
@token_required
def update_user(id: int):
    """Update user."""

    form = request.form.copy().to_dict()
    form["password"] = generate_password_hash(form["password"])
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            UPDATE user SET
                updated_at = CURRENT_TIMESTAMP,
                username = :username,
                password = :password,
                role_id = :role_id
            WHERE id = :id
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "User successfully updated.", 201


@user.delete("/user/<int:id>")
@token_required
def delete_user(id: int):
    """Delete user."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    return "User successfully deleted.", 200
