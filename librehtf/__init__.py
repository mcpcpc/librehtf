#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import makedirs

from flask import Flask
from dash import Dash

from librehtf.api.device import device
from librehtf.api.test import test
from librehtf.api.task import task
from librehtf.api.user import user
from librehtf.cache import create_cache_manager
from librehtf.db import init_app
from librehtf.layout.default import layout
from librehtf.token import init_token


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MAX_CONTENT_LENGTH=16000000,
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
    init_token(app)
    app.register_blueprint(device)
    app.register_blueprint(task)
    app.register_blueprint(test)
    app.register_blueprint(user)
    manager = create_cache_manager(app)
    dashapp = Dash(
        __name__,
        server=app,
        use_pages=True,
        update_title=None,
        background_callback_manager=manager,
    )
    dashapp.layout = layout
    return dashapp.server
