#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import request

from librehtf.auth import login_required
from librehtf.db import get_db

runner = Blueprint("runner", __name__)

query = """
SELECT
    device.name AS device_name,
    device.description AS device_description,
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
    INNER JOIN datatype ON datatype.id = task.datatype_id;
"""


@runner.route("/runner", methods=("GET", "POST"))
@login_required
def index():
    rows = get_db().execute(query).fetchall()
    return render_template("runner.html", rows=rows)