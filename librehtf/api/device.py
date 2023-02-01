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
    """Create device."""

    if not request.form.get("name"):
        return "Name is required.", 400
    elif not request.form.get("description"):
        return "Description is required.", 400
    try:
        db = get_db()
        db.execute(
            "INSERT INTO device (name, description) VALUES (?, ?)",
            (
                request.form.get("name"),
                request.form.get("description"),
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "Device already exists.", 400
    else:
        return "Device successfully created.", 201


@device.route("/device/<int:id>", methods=("GET",))
@token_required
def read_device(id: int):
    """Read device."""

    row = get_db().execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    if not row:
        return "Device does not exist.", 404
    return dict(row)


@device.route("/device/<int:id>", methods=("PUT",))
@token_required
def update_device(id: int):
    """Update device."""

    if not request.form.get("name"):
        return "Name is required.", 400
    elif not request.form.get("description"):
        return "Description is required.", 400
    try:
        db = get_db()
        db.execute(
            "UPDATE device SET name = ?, description = ? WHERE id = ?",
            (request.form.get("name"), request.form.get("description"), id),
        )
        db.commit()
    except db.IntegrityError:
        return "Device already exists.", 400
    else:
        return "Device successfully updated.", 201


@device.route("/device/<int:id>", methods=("DELETE",))
@token_required
def delete_device(id: int):
    """Delete device."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM device WHERE id = ?", (id,))
    db.commit()
    return "Device successfully deleted.", 200
