#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.auth import token_required

device = Blueprint("device", __name__, url_prefix="/api")


@device.route("/device", methods=("POST",))
@token_required
def create_device():
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["description"]:
        return {"message": "Description is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO device (name, description) VALUES (?, ?)",
            (request.form["name"], request.form["description"]),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device already exists."}, 401
    else:
        return {"message": "Device successfully created."}, 201


@device.route("/device/<int:id>", methods=("GET",))
@token_required
def read_device(id: int):
    device = get_db().execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    if not device:
        return {"message": "Device does not exist."}, 401
    return dict(device)


@device.route("/device/<int:id>", methods=("POST",))
@token_required
def update_device(id: int):
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["description"]:
        return {"message": "Description is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE device SET name = ?, description = ? WHERE id = ?",
            (request.form["name"], request.form["description"], id),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device already exists."}, 401
    else:
        return {"message": "Device successfully updated."}, 201


@device.route("/device/<int:id>", methods=("DELETE",))
@token_required
def delete_device(id: int):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM device WHERE id = ?", (id,))
    db.commit()
    return {"message": "Device successfully deleted."}
