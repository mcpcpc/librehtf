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
    """Create task."""

    if not request.form.get("name"):
        return "Name is required.", 400
    elif not request.form.get("command"):
        return "Command is required.", 400
    elif not request.form.get("test_id"):
        return "Test ID is required.", 400
    elif not request.form.get("operator_id"):
        return "Operator ID is required.", 400
    elif not request.form.get("datatype_id"):
        return "Datatype ID is required.", 400
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "INSERT INTO task (name, reference, unit, command, test_id, operator_id, datatype_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                request.form.get("name"),
                request.form.get("reference", None),
                request.form.get("unit", None),
                request.form.get("command"),
                request.form.get("test_id"),
                request.form.get("operator_id"),
                request.form.get("datatype_id"),
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "Task already exists or test, operator or datatype ID invalid.", 400
    else:
        return "Task successfully created.", 201


@task.route("/task/<int:id>", methods=("GET",))
@token_required
def read_task(id: int):
    """Read task."""

    row = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    if not row:
        return "Task does not exist.", 404
    return dict(row)


@task.route("/task/<int:id>", methods=("PUT",))
@token_required
def update_task(id: int):
    """Update task."""

    if not request.form.get("name"):
        return "Name is required.", 400
    elif not request.form.get("command"):
        return "Command is required.", 400
    elif not request.form.get("test_id"):
        return "Test ID is required.", 400
    elif not request.form.get("operator_id"):
        return "Operator ID is required.", 400
    elif not request.form.get("datatype_id"):
        return "Datatype ID is required.", 400
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            "UPDATE task SET name = ?, reference = ?, unit = ?, command = ?, test_id = ?, operator_id = ?, datatype_id = ? WHERE id = ?",
            (
                request.form.get("name"),
                request.form.get("reference", None),
                request.form.get("unit", None),
                request.form.get("command"),
                request.form.get("test_id"),
                request.form.get("operator_id"),
                request.form.get("datatype_id"),
                id,
            ),
        )
        db.commit()
    except db.IntegrityError:
        return "Task already exists or test, operator or datatype ID invalid.", 400
    else:
        return "Task successfully updated.", 201


@task.route("/task/<int:id>", methods=("DELETE",))
@token_required
def delete_task(id: int):
    """Delete task."""

    db = get_db()
    db.execute("DELETE FROM task WHERE id = ?", (id,))
    db.commit()
    return "Task successfully deleted.", 200
