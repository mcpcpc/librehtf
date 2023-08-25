#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.token import token_required

test = Blueprint("test", __name__, url_prefix="/api")


@test.post("/test")
@token_required
def create_test():
    """Create test."""

    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            INSERT INTO test (
                name,
                description,
                device_id
            ) VALUES (
                :name,
                :description,
                :device_id
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Test successfully created.", 201


@test.get("/test/<int:id>")
@token_required
def read_test(id: int):
    """Read test."""

    row = get_db().execute(
        "SELECT * FROM test WHERE id = ?",
        (id,),
    ).fetchone()
    if not row:
        return "Test does not exist.", 404
    return dict(row), 200


@test.put("/test/<int:id>")
@token_required
def update_test(id: int):
    """Update test."""

    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            UPDATE test SET
                updated_at = CURRENT_TIMESTAMP,
                name = :name,
                description = :description,
                device_id = :device_id
            WHERE id = :id
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Test successfully updated.", 201


@test.delete("/test/<int:id>")
@token_required
def delete_test(id: int):
    """Delete test."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM test WHERE id = ?", (id,))
    db.commit()
    return "Test successfully deleted.", 200


@test.get("/test")
@token_required
def list_tests():
    """List tests."""

    rows = get_db().execute(
        "SELECT * FROM test",
    ).fetchall()
    if not rows:
        return "Tests do not exist.", 404
    return list(map(dict, rows)), 200
