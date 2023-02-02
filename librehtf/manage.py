#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

from librehtf.api.device import create_device as api_create_device
from librehtf.api.device import update_device as api_update_device
from librehtf.api.device import delete_device as api_delete_device
from librehtf.api.test import create_test as api_create_test
from librehtf.api.test import update_test as api_update_test
from librehtf.api.test import delete_test as api_delete_test
from librehtf.api.task import create_task as api_create_task
from librehtf.api.task import update_task as api_update_task
from librehtf.api.task import delete_task as api_delete_task
from librehtf.api.user import create_user as api_create_user
from librehtf.api.user import update_user as api_update_user
from librehtf.api.user import delete_user as api_delete_user
from librehtf.auth import login_required
from librehtf.db import get_db

manage = Blueprint("manage", __name__)


@manage.route("/manage", methods=("GET",))
@login_required(permissions=[1, 2])
def index():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template(
        "manage.html", users=users, devices=devices, tests=tests, tasks=tasks
    )


@manage.route("/manage/device/create", methods=("GET", "POST"))
@login_required(permissions=[1])
def create_device():
    if request.method == "POST":
        response = api_create_device.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    return render_template("manage/create_device.html")


@manage.route("/manage/test/create", methods=("GET", "POST"))
@login_required(permissions=[1])
def create_test():
    if request.method == "POST":
        response = api_create_test.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    devices = get_db().execute("SELECT * FROM device").fetchall()
    return render_template("manage/create_test.html", devices=devices)


@manage.route("/manage/task/create", methods=("GET", "POST"))
@login_required(permissions=[1])
def create_task():
    if request.method == "POST":
        response = api_create_task.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    return render_template(
        "manage/create_task.html", tests=tests, operators=operators, datatypes=datatypes
    )


@manage.route("/manage/user/create", methods=("GET", "POST"))
@login_required(permissions=[1])
def create_user():
    if request.method == "POST":
        response = api_create_user.__wrapped__()
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    return render_template("manage/create_user.html")


@manage.route("/manage/device/<int:id>/update", methods=("GET", "POST"))
@login_required(permissions=[3])
def update_device(id: int):
    if request.method == "POST":
        response = api_update_device.__wrapped__(id)
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    row = get_db().execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    return render_template("manage/update_device.html", row=row)


@manage.route("/manage/test/<int:id>/update", methods=("GET", "POST"))
@login_required(permissions=[3])
def update_test(id: int):
    if request.method == "POST":
        response = api_update_test.__wrapped__(id)
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    db = get_db()
    row = db.execute("SELECT * FROM test WHERE id = ?", (id,)).fetchone()
    devices = db.execute("SELECT * FROM device").fetchall()
    return render_template("manage/update_test.html", row=row, devices=devices)


@manage.route("/manage/task/<int:id>/update", methods=("GET", "POST"))
@login_required(permissions=[3])
def update_task(id: int):
    if request.method == "POST":
        response = api_update_task.__wrapped__(id)
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    db = get_db()
    row = db.execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    tests = db.execute("SELECT * FROM test").fetchall()
    operators = db.execute("SELECT * FROM operator").fetchall()
    datatypes = db.execute("SELECT * FROM datatype").fetchall()
    return render_template(
        "manage/update_task.html",
        row=row,
        tests=tests,
        operators=operators,
        datatypes=datatypes,
    )


@manage.route("/manage/user/<int:id>/update", methods=("GET", "POST"))
@login_required(permissions=[3])
def update_user(id: int):
    if request.method == "POST":
        response = api_update_user.__wrapped__(id)
        if response[1] < 300:
            return redirect(url_for(".index"))
        flash(response[0], "error")
    db = get_db()
    row = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    roles = db.execute("SELECT * FROM role").fetchall()
    return render_template("manage/update_user.html", row=row, roles=roles)


@manage.route("/manage/device/<int:id>/delete", methods=("GET",))
@login_required(permissions=[4])
def delete_device(id: int):
    response = api_delete_device.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/test/<int:id>/delete", methods=("GET",))
@login_required(permissions=[4])
def delete_test(id: int):
    response = api_delete_test.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/task/<int:id>/delete", methods=("GET",))
@login_required(permissions=[4])
def delete_task(id: int):
    response = api_delete_task.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    return redirect(url_for(".index"))


@manage.route("/manage/user/<int:id>/delete", methods=("GET",))
@login_required(permissions=[4])
def delete_user(id: int):
    response = api_delete_user.__wrapped__(id)
    if response[1] >= 300:
        flash(response[0], "error")
    if g.user["id"] == id:
        redirect(url_for("auth.logout"))
    return redirect(url_for(".index"))
