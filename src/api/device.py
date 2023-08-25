#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from db import get_db
from token import token_required

device = Blueprint("device", __name__, url_prefix="/api")


@device.post("/device")
@token_required
def create_device():
    """Create device."""

    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute(
            """
            INSERT INTO device (
                name,
                description
            ) VALUES (
                :name,
                :description
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Device successfully created.", 201


@device.get("/device/<int:id>")
@token_required
def read_device(id: int):
    """Read device."""

    row = get_db().execute(
        "SELECT * FROM device WHERE id = ?",
        (id,),
    ).fetchone()
    if not row:
        return "Device does not exist.", 404
    return dict(row), 200


@device.put("/device/<int:id>")
@token_required
def update_device(id: int):
    """Update device."""

    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute(
            """
            UPDATE device SET
                updated_at = CURRENT_TIMESTAMP,
                name = :name,
                description = :description
            WHERE id = :id
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Device successfully updated.", 201


@device.delete("/device/<int:id>")
@token_required
def delete_device(id: int):
    """Delete device."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM device WHERE id = ?", (id,))
    db.commit()
    return "Device successfully deleted.", 200


@device.get("/device")
@token_required
def list_devices():
    """List devices."""

    rows = get_db().execute(
        "SELECT * FROM device",
    ).fetchall()
    if not rows:
        return "Devices do not exist.", 404
    return list(map(dict, rows)), 200
