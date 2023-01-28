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
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template("manage.html", devices=devices, tests=tests, tasks=tasks)


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
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if request.method == "POST":
        if api == "device":
            resp = create_device.__wrapped__()
            print(resp)
        elif api == "test":
            resp = create_test.__wrapped__()
            print(resp)
        elif api == "task":
            resp = create_task.__wrapped__()
            print(resp)
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


@manage.route("/manage/<api>/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(api: str, id: int):
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    if request.method == "POST":
        if api == "device":
            resp = update_device.__wrapped__(id)
            print(resp)
        elif api == "test":
            resp = update_test.__wrapped__(id)
            print(resp)
        elif api == "task":
            resp = update_task.__wrapped__(id)
            print(resp)
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