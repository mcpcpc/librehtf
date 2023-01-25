#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.auth import token_required

task = Blueprint("task", __name__, url_prefix="/api")


@task.route("/task", methods=("POST",))
@token_required
def create_task():
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["command"]:
        return {"message": "Command is required."}, 401
    elif not request.form["test_id"]:
        return {"message": "Test ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO task (name, command, test_id) VALUES (?, ?, ?)",
            (request.form["name"], request.form["command"], request.form["test_id"]),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Test ID does not exist."}, 401
    else:
        return {"message": "Task successfully created."}, 201


@task.route("/task/<int:id>", methods=("GET",))
@token_required
def read_task(id: int):
    task = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    if not task:
        return {"message": "Task does not exist"}, 401
    return dict(task)


@task.route("/task/<int:id>", methods=("POST",))
@token_required
def update_task(id: int):
    if not request.form["name"]:
        return {"message": "Name is required."}, 401
    elif not request.form["command"]:
        return {"message": "Command is required."}, 401
    elif not request.form["test_id"]:
        return {"message": "Test ID is required."}, 401
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE task SET test_id = ?, name = ?, command = ? WHERE id = ?",
            (request.form["test_id"], request.form["name"], request.form["command"], id),
        )
        db.commit()
    except db.IntegrityError:
        return {"message": "Test ID does not exist."}, 401
    else:
        return {"message": "Task successfully updated."}, 201


@task.route("/task/<int:id>", methods=("DELETE",))
@token_required
def delete_task(id: int):
    db = get_db()
    db.execute("DELETE FROM task WHERE id = ?", (id,))
    db.commit()
    return {"message": "Task successfully deleted."}
