#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import makedirs

from flask import Flask
from flask import render_template

from librehtf.api.device import device
from librehtf.api.test import test
from librehtf.api.task import task
from librehtf.api.user import user
from librehtf.auth import auth
from librehtf.db import init_app
from librehtf.evaluate import evaluate
from librehtf.manage import manage


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=path.join(app.instance_path, "librehtf.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    try:
        makedirs(app.instance_path)
    except OSError:
        pass
    init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(device)
    app.register_blueprint(evaluate)
    app.register_blueprint(manage)
    app.register_blueprint(test)
    app.register_blueprint(task)
    app.register_blueprint(user)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html")

    app.add_url_rule("/", endpoint="index")
    return app
