#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import request

from librehtf.auth import login_required
from librehtf.db import get_db

evaluate = Blueprint("evaluate", __name__)

query = """
SELECT
    device.name AS device_name,
    device.description AS device_description,
    test.id AS test_id,
    test.name AS test_name,
    test.description AS test_description,
    task.id AS task_id,
    task.name AS task_name,
    task.unit AS task_unit,
    task.reference AS task_reference,
    task.command AS task_command,
    operator.slug AS operator_slug,
    datatype.slug AS datatype_slug
FROM device
    INNER JOIN test ON test.device_id = device.id
    INNER JOIN task ON task.test_id = test.id
    INNER JOIN operator ON operator.id = task.operator_id
    INNER JOIN datatype ON datatype.id = task.datatype_id
"""


def measure(command: str):
    result = {}
    cc = compile(command, "<string>", "exec")
    exec(cc, globals(), result)
    return result


@evaluate.route("/evaluate", methods=("GET",))
@login_required
def index():
    rows = get_db().execute(query).fetchall()
    return render_template("evaluate.html", rows=rows)


@evaluate.route("/evaluate/<int:test_id>", methods=("GET",))
@login_required
def run(test_id: int):
    rows = get_db().execute(query + " WHERE test_id = ?", (test_id,)).fetchone()
    results = {}
    for row in rows:
        measured = measure(row["command"])
        if "measured" not in measured:
            return "Invalid command.", 400
        results[row["task_id"]] = measured
    return results
