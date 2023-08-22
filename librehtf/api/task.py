#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from librehtf.db import get_db
from librehtf.token import token_required

task = Blueprint("task", __name__, url_prefix="/api")


@task.post("/task")
@token_required
def create_task():
    """Create task."""

    form = request.form.copy().to_dict()
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            INSERT INTO task (
                name,
                reference,
                unit,
                command,
                test_id,
                operator_id,
                datatype_id
            ) VALUES (
                :name,
                :reference,
                :unit,
                :command,
                :test_id,
                :operator_id,
                :datatype_id
            )
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Task successfully created.", 201


@task.get("/task/<int:id>")
@token_required
def read_task(id: int):
    """Read task."""

    row = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    if not row:
        return "Task does not exist.", 404
    return dict(row)


@task.put("/task/<int:id>")
@token_required
def update_task(id: int):
    """Update task."""

    form = request.form.copy().to_dict()
    form["id"] = id
    try:
        db = get_db()
        db.execute("PRAGMA foreign_keys = ON")
        db.execute(
            """
            UPDATE task SET
                updated_at = CURRENT_TIMESTAMP,
                name = :name,
                reference = :reference,
                unit = :unit,
                command = :command,
                test_id = :test_id,
                operator_id = :operator_id,
                datatype_id = :datatype_id
            WHERE id = ?
            """,
            form,
        )
        db.commit()
    except db.ProgrammingError:
        return "Missing parameter(s).", 400
    except db.IntegrityError:
        return "Invalid parameter(s).", 400
    return "Task successfully updated.", 201


@task.delete("/task/<int:id>")
@token_required
def delete_task(id: int):
    """Delete task."""

    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM task WHERE id = ?", (id,))
    db.commit()
    return "Task successfully deleted.", 200
