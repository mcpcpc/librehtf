#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.auth import token_required

test = Blueprint("test", __name__, url_prefix="/api")


@test.route("/test", methods=("POST",))
@token_required
def create_test():
    """Create test."""

    if not request.form.get("name"):
        return "Name is required.", 400
    elif not request.form.get("description"):
        return "Description is required.", 400
    elif not request.form.get("device_id"):
        return "Device ID is required.", 400
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO test (name, description, device_id) VALUES (?, ?, ?)",
            (
                request.form.get("name"),
                request.form.get("description"),
                request.form.get("device_id"),
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "Test already exists or device ID invalid.", 400
    else:
        return "Test successfully created.", 201


@test.route("/test/<int:id>", methods=("GET",))
@token_required
def read_test(id: int):
    """Read test."""

    row = get_db().execute("SELECT * FROM test WHERE id = ?", (id,)).fetchone()
    if not row:
        return "Test does not exist.", 404
    return dict(row)


@test.route("/test/<int:id>", methods=("PUT",))
@token_required
def update_test(id: int):
    """Update test."""

    if not request.form["name"]:
        return "Name is required.", 400
    elif not request.form.get("description"):
        return "Description is required.", 400
    elif not request.form.get("device_id"):
        return "Device ID is required.", 400
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE test SET name = ?, description = ?, device_id = ? WHERE id = ?",
            (
                request.form.get("name"),
                request.form.get("description"),
                request.form.get("device_id"),
                id,
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "Test already exists or device ID invalid.", 400
    else:
        return "Test successfully updated.", 201


@test.route("/test/<int:id>", methods=("DELETE",))
@token_required
def delete_test(id: int):
    """Delete test."""

    db = get_db()
    db.execute("DELETE FROM test WHERE id = ?", (id,))
    db.commit()
    return "Test successfully deleted.", 200
