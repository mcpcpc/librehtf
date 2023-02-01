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
from librehtf.device import create_device as api_create_device
from librehtf.device import update_device as api_update_device
from librehtf.device import delete_device as api_delete_device
from librehtf.test import create_test as api_create_test
from librehtf.test import update_test as api_update_test
from librehtf.test import delete_test as api_delete_test
from librehtf.task import create_task as api_create_task
from librehtf.task import update_task as api_update_task
from librehtf.task import delete_task as api_delete_task

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


@manage.route("/manage/device/<int:id>/delete", methods=("GET",))
@login_required
def delete_device(id: int):
    response = api_delete_device.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/test/<int:id>/delete", methods=("GET",))
@login_required
def delete_test(id: int):
    response = api_delete_test.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/task/<int:id>/delete", methods=("GET",))
@login_required
def delete_task(id: int):
    response = api_delete_task.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/device/create", methods=("GET", "POST"))
@login_required
def create_device(api: str):
    if request.method == "POST":
        response = api_create_device.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0])
    return render_template("manage/create_device.html")


@manage.route("/manage/test/create", methods=("GET", "POST"))
@login_required
def create_test(api: str):
    if request.method == "POST":
        response = api_create_test.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0])
    devices = get_db().execute("SELECT * FROM device").fetchall()
    return render_template("manage/create_test.html",  devices=devices)


@manage.route("/manage/task/create", methods=("GET", "POST"))
@login_required
def create_task(api: str):
    if request.method == "POST":
        response = api_create_task.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0])
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    return render_template("manage/create_task.html", tests=tests, operators=operators, datatypes=datatypes)


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
            resp = api_update_device.__wrapped__(id)
        elif api == "test":
            resp = api_update_test.__wrapped__(id)
        elif api == "task":
            resp = api_update_task.__wrapped__(id)
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
