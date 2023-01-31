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

    def test_register_get(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.get("/auth/register")
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.post(
            "/auth/register",
            data={"username": "user1", "password": "pass1"},
        )
        self.assertEqual(response.headers["location"], "/auth/login")

    def test_register_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        parameters = [
            ("", "", b"Username is required."),
            ("user1", "", b"Password is required."),
            ("test", "test", b"test already exists."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                username, password, message = parameter
                response = self.client.post(
                    "/auth/register",
                    data={
                        "username": username,
                        "password": password,
                    },
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_update_get(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.get("/auth/2/update")
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.post("/auth/2/update", data={"role_id": 3, "password": "pass1_"})
        self.assertEqual(response.headers["location"], "/auth/login")

    def test_update_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        parameters = [
            ("", "pass1_", b"RoleID is required."),
            (2, "", b"Password is required."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                role_id, password, message = parameter
                response = self.client.post(
                    "/auth/2/update",
                    data={"": role_id, "password": password},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_delete(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.get("/auth/2/delete")
        self.assertEqual(response.headers["location"], "/")

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
