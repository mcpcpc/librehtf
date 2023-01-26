#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from librehtf.db import get_db
from librehtf.auth import login_required

manage = Blueprint("manage", __name__)

@manage.route("/manage", methods=("GET",))
@login_required
def manager():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    devices = db.execute("SELECT * FROM device").fetchall()
    tests = db.execute("SELECT * FROM test").fetchall()
    tasks = db.execute("SELECT * FROM task").fetchall()
    return render_template("manage.html", devices=devices, tests=tests, tasks=tasks)
