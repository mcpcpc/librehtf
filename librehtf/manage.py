#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
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
        response = delete_device()
    elif api == "test":
        response = delete_test()
    elif api == "task":
        response = delete_task()
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
            response = create_device()
        elif api == "test":
            response = create_test()
        elif api == "task":
            response = create_task()
        print(response) 
    return render_template(
        "manage/create.html",
        api=api,
        tests=tests,
        devices=devices,
        operators=operators,
        datatypes=datatypes,
    )