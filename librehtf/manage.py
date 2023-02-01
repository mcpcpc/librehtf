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
from librehtf.device import create_device
from librehtf.device import update_device
from librehtf.device import delete_device
from librehtf.test import create_test
from librehtf.test import update_test
from librehtf.test import delete_test
from librehtf.task import create_task
from librehtf.task import update_task
from librehtf.task import delete_task

manage = Blueprint("manage", __name__)


@manage.route("/manage", methods=("GET",))
@login_required
def index():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template(
        "manage.html", users=users, devices=devices, tests=tests, tasks=tasks
    )


@manage.route("/manage/<api>/<int:id>/delete", methods=("GET",))
@login_required
def delete(api: str, id: int):
    if api == "device":
        resp = delete_device.__wrapped__(id)
    elif api == "test":
        resp = delete_test.__wrapped__(id)
    elif api == "task":
        resp = delete_task.__wrapped__(id)
    else:
        flash("Invalid endpoint.", "error")
    return redirect(url_for(".index"))


@manage.route("/manage/<api>/create", methods=("GET", "POST"))
@login_required
def create(api: str):
    error = None
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if request.method == "POST":
        if api == "device":
            resp = create_device.__wrapped__()
        elif api == "test":
            resp = create_test.__wrapped__()
        elif api == "task":
            resp = create_task.__wrapped__()
        else:
            error = "Invalid endpoint."
        if resp[1] >= 300:
            error = resp[0]
        if error is None:
            return redirect(url_for(".index"))
        flash(error, "error")
    return render_template(
        "manage/create.html",
        api=api,
        tests=tests,
        devices=devices,
        operators=operators,
        datatypes=datatypes,
    )


@manage.route("/manage/<api>/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(api: str, id: int):
    error = None
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if api == "device":
        row = db.execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    elif api == "test":
        row = db.execute("SELECT * FROM test WHERE id = ?", (id,)).fetchone()
    elif api == "task":
        row = db.execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        if api == "device":
            resp = update_device.__wrapped__(id)
        elif api == "test":
            resp = update_test.__wrapped__(id)
        elif api == "task":
            resp = update_task.__wrapped__(id)
        else:
            error = "Invalid endpoint."
        if resp[1] >= 300:
            error = resp[0]
        if error is None:
            return redirect(url_for(".index"))
        flash(error, "error")
    return render_template(
        "manage/update.html",
        api=api,
        row=row,
        tests=tests,
        devices=devices,
        operators=operators,
        datatypes=datatypes,
    )
