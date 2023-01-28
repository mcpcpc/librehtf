#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

from librehtf.auth import login_required
from librehtf.db import get_db

manage = Blueprint("manage", __name__)


@manage.route("/manage", methods=("GET", "POST"))
@login_required
def index():
    devices = get_db().execute("SELECT * FROM device").fetchall()
    tests = get_db().execute("SELECT * FROM test").fetchall()
    tasks = get_db().execute("SELECT * FROM task").fetchall()
    return render_template("manage.html", devices=devices, tests=tests, tasks=tasks)


@manage.route("/manage/<api>/<int:id>/delete", methods=("GET",))
@login_required
def delete(api: str, id: int):
    db = get_db()
    if api == "device":
        db.execute("DELETE FROM device WHERE id = ?", (id,))
        db.commit()
    elif api == "test":
        db.execute("DELETE FROM test WHERE id = ?", (id,))
        db.commit()
    elif api == "task":
        db.execute("DELETE FROM test WHERE id = ?", (id,))
        db.commit()
    else:
        flash("Invalid API", "error")
    return redirect(url_for(".index"))


@manage.route("/manage/<api>/create", methods=("GET", "POST"))
@login_required
def create(api: str):
    db = get_db()
    if request.method == "POST":
        pass
    return render_template("manage/create.html", api=api)