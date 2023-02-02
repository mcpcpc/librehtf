#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from flask import session

from librehtf import create_app


class AuthTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._resources = Path(__file__).parent
        path = cls._resources / "preload.sql"
        with open(path, mode="r", encoding="utf-8") as f:
            cls._preload = f.read()

    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app(
            {"TESTING": True, "DATABASE": self.db, "SECRET_KEY": "dev"}
        )
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_login_protected_endpoints(self):
        db = connect(self.db)
        db.executescript(self._preload)
        parameters = ("/auth/token",)
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                response = self.client.get(parameter)
                self.assertEqual(response.headers["Location"], "/auth/login")

    def test_login_get(self):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.post(
            "/auth/login", data={"username": "test", "password": "test"}
        )
        self.assertEqual(response.headers["location"], "/")

    def test_login_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        parameters = [
            ("test1", "test", b"Incorrect username or password."),
            ("test", "test1", b"Incorrect username or password."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                username, password, message = parameter
                response = self.client.post(
                    "/auth/login",
                    data={"username": username, "password": password},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_token_get(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.get("/auth/token")
        self.assertEqual(response.status_code, 200)

    def test_token_post(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.post("/auth/token", data={"expires_in": 600})
        self.assertIn("access_token", response.json)

    def test_token_post_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        parameters = [
            ("", b"Expiration is required."),
            ("a", b"Expiration is not numeric."),
            (31536001, b"Expiration too big."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                expires_in, message = parameter
                response = self.client.post(
                    "/auth/token",
                    data={"expires_in": expires_in},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)


if __name__ == "__main__":
    main()
