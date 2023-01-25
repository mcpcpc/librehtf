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
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["description"]:
        return {"message": "Description is required."}, 401
    elif not request.form["device_id"]:
        return {"message": "Device ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO test (name, description, device_id) VALUES (?, ?, ?)",
            (request.form["name"], request.form["description"], request.form["device_id"]),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device ID does not exist."}, 401
    else:
        return {"message": "Test successfully created."}, 201


@test.route("/test/<int:id>", methods=("GET",))
@token_required
def read_test(id: int):
    row = get_db().execute("SELECT * FROM test WHERE id = ?", (id,)).fetchone()
    if not row:
        return {"message": "Test does not exist"}, 401
    return dict(row)


@test.route("/test/<int:id>", methods=("POST",))
@token_required
def update_test(id: int):
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["description"]:
        return {"message": "Description is required."}, 401
    elif not request.form["device_id"]:
        return {"message": "Device ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE test SET device_id = ?, name = ?, description = ? WHERE id = ?",
            (request.form["device_id"], request.form["name"], request.form["description"], id),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device ID does not exist."}, 401
    else:
        return {"message": "Test successfully updated."}, 201


@test.route("/test/<int:id>", methods=("DELETE",))
@token_required
def delete_test(id: int):
    db = get_db()
    db.execute("DELETE FROM test WHERE id = ?", (id,))
    db.commit()
    return {"message": "Test successfully deleted."}
