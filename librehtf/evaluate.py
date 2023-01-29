#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import request

from librehtf.auth import login_required
from librehtf.db import get_db

evaluate = Blueprint("evaluate", __name__)

query_devices = """
SELECT
    device.name AS device_name,
    device.description AS device_description,
    test.id AS test_id,
    test.name AS test_name,
    test.description AS test_description
FROM device
    INNER JOIN test ON test.device_id = device.id
"""

query_test_id = """
SELECT
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
FROM test
    INNER JOIN task ON task.test_id = test.id
    INNER JOIN operator ON operator.id = task.operator_id
    INNER JOIN datatype ON datatype.id = task.datatype_id
WHERE
    test_id = ? 
"""


def measure(command: str):
    result = {}
    cc = compile(command, "<string>", "exec")
    exec(cc, globals(), result)
    return result


@evaluate.route("/evaluate", methods=("GET",))
@login_required
def index():
    rows = get_db().execute(query_devices).fetchall()
    return render_template("evaluate.html", rows=rows)


@evaluate.route("/evaluate/<int:test_id>", methods=("GET",))
@login_required
def results(test_id: int):
    rows = get_db().execute(query_test_id, (test_id,)).fetchall()
    if rows is None:
        return "Invalid test identifier.", 400
    results = []
    for row in rows:
        result = row.copy()
        result = measure(row["task_command"])
        if "measured" not in result:
            return "Invalid command.", 400
        result["test_name"] = row["test_name"]
        result["task_name"] = row["task_name"]
        result["test_description"] = row["test_description"]
        result["observation"] = "INFO" # temporary
        results.append(result)
    print(results)
    return render_template("evaluate/results.html", results=results)
