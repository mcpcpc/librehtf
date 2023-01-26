#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from librehtf.db import get_db
from librehtf.auth import login_required

manage = Blueprint("manage", __name__)

@manage.route("/manage", methods=("GET",))
@login_required
def index():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template("manage.html", devices=devices, tests=tests, tasks=tasks, users=users)

@manage.route("/manage/create", methods=("GET",))
@login_required
def create():
     db = get_db()
    if request.args.get("api") == "device":
        devices = db.execute("SELECT * FROM device").fetchall()
        return render_template("manage/create.html", devices=devices, api="device")
    elif request.args.get("api") == "test":
        tests = db.execute("SELECT * FROM test").fetchall()
        return render_template("manage/create.html", tests=tests, api="test")
    elif request.args.get("api") == "task":
        tasks = db.execute("SELECT * FROM task").fetchall()
        return render_template("manage/create.html", tasks=tasks, api="task")
    flash("API argument invalid", "error")
    return redirect(url_for("manage.index"))
