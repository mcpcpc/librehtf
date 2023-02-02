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
    exec(cc, {}, result)
    return result


@evaluate.route("/evaluate", methods=("GET",))
@login_required(permissions=None)
def index():
    rows = get_db().execute(query_devices).fetchall()
    return render_template("evaluate.html", rows=rows)


@evaluate.route("/evaluate/<int:test_id>", methods=("GET",))
@login_required(permissions=None)
def results(test_id: int):
    rows = get_db().execute(query_test_id, (test_id,)).fetchall()
    if rows is None:
        return "Invalid test identifier.", 400
    results = []
    for row in rows:
        result = dict(row)
        try:
            measured = measure(row["task_command"])
        except SyntaxError:
            return "Command string contains syntax error.", 400
        if "measured" not in measured:
            return "Measure value is missing from result.", 400
        result["measured"] = measured["measured"]
        if row["operator_slug"] != "none":
            datatype = __builtins__[row["datatype_slug"]]
            operator = getattr(datatype, row["operator_slug"])
            reference = row["task_reference"]
            value = measured["measured"]
            if operator(datatype(value), datatype(reference)):
                result["observation"] = "PASS"
            else:
                result["observation"] = "FAIL"
        else:
            result["observation"] = "INFO"
        results.append(result)
    if "raw" in request.args:
        return results
    return render_template("evaluate/results.html", results=results)
