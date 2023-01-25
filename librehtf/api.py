#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.auth import token_required

api = Blueprint("api", __name__, url_prefix="/api")


@api.post("/task")
@token_required
def create_task():
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["command"]:
        return {"message": "Command is required."}, 401
    elif not request.form["device_id"]:
        return {"message": "Device ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO task (name, command, device_id) VALUES (?, ?, ?)",
            (request.form["name"], request.form["command"], request.form["device_id"]),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device ID does not exist."}, 401
    else:
        return {"message": "Task successfully created."}, 201


@api.get("/task/<int:id>")
@token_required
def read_task(id: int):
    task = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    if not task:
        return {"message": "Task does not exist"}, 401
    return dict(task)


@api.post("/task/<int:id>")
@token_required
def update_task(id: int):
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["command"]:
        return {"message": "Command is required."}, 401
    elif not request.form["device_id"]:
        return {"message": "Device ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE task SET device_id = ?, name = ?, command = ? WHERE id = ?",
            (request.form["device_id"], request.form["name"], request.form["command"], id),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Device ID does not exist."}, 401
    else:
        return {"message": "Task successfully updated."}, 201


@api.delete("/task/<int:id>")
@token_required
def delete_task(id: int):
    db = get_db()
    db.execute("DELETE FROM task WHERE id = ?", (id,))
    db.commit()
    return {"message": "Task successfully deleted."}


@api.post("/device")
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


@api.get("/device/<int:id>")
@token_required
def read_device(id: int):
    device = get_db().execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    if not device:
        return {"message": "Device does not exist."}, 401
    return dict(device)


@api.post("/device/<int:id>")
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


@api.delete("/device/<int:id>")
@token_required
def delete_device(id: int):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM device WHERE id = ?", (id,))
    db.commit()
    return {"message": "Device successfully deleted."}
