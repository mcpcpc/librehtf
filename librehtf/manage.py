#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

from librehtf.auth import login_required
from librehtf.db import get_db
from librehtf.device import delete_device

manage = Blueprint("manage", __name__)


@manage.route("/manage", methods=("GET",))
@login_required
def index():
    db = get_db()
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template("manage.html", devices=devices, tests=tests, tasks=tasks)


@manage.route("/manage/<api>/<int:id>/delete", methods=("GET",))
@login_required
def delete(api: str, id: int):
    if api == "device":
        resp = delete_device.__wrapped__(id)
        print(resp)
        # db.execute("DELETE FROM device WHERE id = ?", (id,))
        # db.commit()
    elif api == "test":
        db = get_db()
        db.execute("DELETE FROM test WHERE id = ?", (id,))
        db.commit()
    elif api == "task":
        db = get_db()
        db.execute("DELETE FROM task WHERE id = ?", (id,))
        db.commit()
    else:
        flash("Invalid endpoint.", "error")
    return redirect(url_for(".index"))


@manage.route("/manage/<api>/create", methods=("GET", "POST"))
@login_required
def create(api: str):
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if request.method == "POST":
        if api == "device":
            db = get_db()
            db.execute("PRAGMA foreign_keys = ON")
            db.execute(
                "INSERT INTO device (name, description) VALUES (?, ?)",
                (
                    request.form.get("name"),
                    request.form.get("description"),
                ),
            )
            db.commit()
        elif api == "test":
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
        elif api == "task":
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
        else:
            flash("Invalid endpoint.", "error")
        return redirect(url_for(".index"))
    return render_template(
        "manage/create.html",
        api=api,
        tests=tests,
        devices=devices,
        operators=operators,
        datatypes=datatypes,
    )


@manage.route("/manage/<api>/update", methods=("GET", "POST"))
@login_required
def update(api: str):
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if request.method == "POST":
        if api == "device":
            db = get_db()
            db.execute("PRAGMA foreign_keys = ON")
            db.execute(
                "UPDATE device SET name = ?, description = ? WHERE id = ?",
                (
                    request.form.get("name"),
                    request.form.get("description"),
                    id
                ),
            )
            db.commit()
        elif api == "test":
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
        elif api == "task":
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
        else:
            flash("Invalid endpoint.", "error")
        return redirect(url_for(".index"))
    return render_template(
        "manage/create.html",
        api=api,
        tests=tests,
        devices=devices,
        operators=operators,
        datatypes=datatypes,
    )