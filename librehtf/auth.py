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

def auth_required(view):
    """Authorization required wrapper."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            if "Authorization" not in request.headers:
                return {"message": "Token required."},  401
            token = request.headers.get("Authorization", None).replace("Bearer ", "")
            secret = current_app.config["SECRET_KEY"]
            try:
                id = decode(token, secret, algorithms=["HS256"])
            except Error as error:
                return {"message": f"{error}"}, 401
            user = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
            if not user:
                return {"message": "Invalid user authentication."}, 401
        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
def load_logged_in_user():
    """Set application context user variable, if not already set."""

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        g.user = user


@auth.route("/login", methods=("GET", "POST"))
def login():
    """User login request."""

    if request.method == "POST":
        error = None
        if not request.form["username"]:
            error = "Username is required."
        if not request.form["password"]:
            error = "Password is required."
        user = get_db().execute(
            "SELECT * FROM user WHERE username = ?", (request.form["username"],)
        ).fetchone()
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
    flash("User successfully logged out.")
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=("GET", "POST"))
@auth_required
def register():
    """Register new user."""

    if request.method == "POST":
        error = None
        if not request.form["username"]:
            error = "Username is required."
        if not request.form["password"]:
            error = "Password is required."
        if error is None:
            hashed_password = generate_password_hash(request.form["password"])
            try:
                db = get_db()
                db.execute(
                    "INSERT INTO user (username, password, role_id) VALUES (?, ?, 3)",
                    (request.form["username"], hashed_password),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {request.form['username']} already exists."
            else:
                flash("User successfully registered.")
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@auth.route("/token", methods=("GET", "POST"))
@auth_required
def token():
    """Generate user token."""

    if request.method == "POST":
        error = None
        expires_in = 600
        if request.form["expiration"]:
            try:
                expires_in = int(request.form["expires_in"])
            except ValueError:
                error = "Expiration value invalid."
        if expires_in > 31536000:
            error = "Expiration too big."
        if error is None:
            expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
            token = encode(
                {"confirm": session.get("user_id"), "exp": expiration},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return {"access_token": token}
        flash(error)
    return render_template("auth/token.html")
