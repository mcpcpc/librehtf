#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import wraps

from click import argument
from click import command
from click import echo
from flask import current_app
from flask import request
from jwt import decode
from jwt import encode


def token_required(view):
    """Token required decorator function."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not request.args.get("token", None):
            return "Token required.", 401
        try:
            id = decode(
                request.args["token"],
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"],
            ).get("confirm")
        except Exception as error:
            return f"{error}", 401
        return view(*args, **kwargs)

    return wrapped_view


@command("token")
@argument("expires_in", type=int, default=300)
def init_token_command(expires_in):
    """
    Initialize and generate new token key given a specified
    expiration timeframe where the default expiration time
    is 300 seconds (5 minutes).
    """

    delta = timedelta(seconds=expires_in)
    exp = datetime.now(tz=timezone.utc) + delta
    token = encode(
        {"confirm": "42", "exp": exp},
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    echo(f"{token}")


def init_token(app):
    """
    Add command to Flask application instance to initialize
    and generate a new token key. 
    """

    app.cli.add_command(init_token_command)
