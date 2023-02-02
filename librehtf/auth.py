#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from jwt import decode
from jwt import encode
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from librehtf.db import get_db

auth = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(permissions: list = None):
    """Login required decorator function."""

    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if g.user is None:
                return redirect(url_for("auth.login"))
            if isinstance(permissions, list):
                role_permission = (
                    get_db()
                    .execute(
                        "SELECT * FROM role_permission WHERE role_id = ?",
                        (g.user["role_id"]),
                    )
                    .fetchall()
                )
                permission_list = [x["permission_id"] for x in role_permission]
                if not all(
                    [permission in permission_list for permission in permissions]
                ):
                    return "User is not authorized to access this endpoint", 401
            return view(*args, **kwargs)

        return wrapped_view

    return decorator


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
        user = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
        if not user:
            return "Invalid user token.", 401
        return view(*args, **kwargs)

    return wrapped_view


@auth.before_app_request
def load_logged_in_user():
    """Set application context user variable, if not already set."""

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@auth.route("/login", methods=("GET", "POST"))
def login():
    """User login request."""

    if request.method == "POST":
        error = None
        if not request.form["username"]:
            error = "Username is required."
        elif not request.form["password"]:
            error = "Password is required."
        user = (
            get_db()
            .execute(
                "SELECT * FROM user WHERE username = ?", (request.form["username"],)
            )
            .fetchone()
        )
        if user is None:
            error = "Incorrect username or password."
        elif not check_password_hash(user["password"], request.form["password"]):
            error = "Incorrect username or password."
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error, "error")
    return render_template("auth/login.html")


@auth.route("/logout", methods=("GET",))
def logout():
    """Clear current session, including the stored user ID."""

    session.clear()
    return redirect(url_for(".login"))


@auth.route("/register", methods=("GET", "POST"))
@login_required(permissions=None)
def register():
    """Register new user."""

    if request.method == "POST":
        error = None
        if not request.form["username"]:
            error = "Username is required."
        elif not request.form["password"]:
            error = "Password is required."
        if error is None:
            hashed_password = generate_password_hash(request.form["password"])
            try:
                db = get_db()
                db.execute("PRAGMA foreign_keys = ON")
                db.execute(
                    "INSERT INTO user (username, password, role_id) VALUES (?, ?, 3)",
                    (request.form["username"], hashed_password),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {request.form['username']} already exists."
            else:
                return redirect(url_for(".login"))
        flash(error)
    return render_template("auth/register.html")


@auth.route("<int:id>/update", methods=("GET", "POST"))
@login_required(permissions=None)
def update(id: int):
    """Update existing user."""

    db = get_db()
    user = db.execute(
        "SELECT username, role_id FROM user WHERE id = ?", (id,)
    ).fetchone()
    roles = db.execute("SELECT * FROM role").fetchall()
    if request.method == "POST":
        error = None
        if not request.form["password"]:
            error = "Password is required."
        elif not request.form["role_id"]:
            error = "Role ID is required."
        if error is None:
            hashed_password = generate_password_hash(request.form["password"])
            try:
                db.execute("PRAGMA foreign_keys = ON")
                db.execute(
                    "UPDATE user SET password = ?, role_id = ? WHERE id = ?",
                    (hashed_password, request.form["role_id"], id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Username or Role ID does not exist."
            else:
                if g.user["id"] == id:
                    return redirect(url_for(".logout"))
                return redirect(url_for(".login"))
        flash(error)
    return render_template("auth/update.html", user=user, roles=roles)


@auth.route("<int:id>/delete", methods=("GET",))
@login_required(permissions=None)
def delete(id: int):
    """Delete existing user."""

    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    if g.user["id"] == id:
        return redirect(url_for(".logout"))
    return redirect(url_for("index"))


@auth.route("/token", methods=("GET", "POST"))
@login_required(permissions=None)
def token():
    """Generate user token."""

    if request.method == "POST":
        error = None
        if not request.form["expires_in"]:
            error = "Expiration is required."
        elif not request.form["expires_in"].isdigit():
            error = "Expiration is not numeric."
        elif int(request.form["expires_in"]) > 31536000:
            error = "Expiration too big."
        if error is None:
            expires_in = int(request.form["expires_in"])
            expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
            token = encode(
                {"confirm": session.get("user_id"), "exp": expiration},
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            return {"access_token": token}
        flash(error)
    return render_template("auth/token.html")
