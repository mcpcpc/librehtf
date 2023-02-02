#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from librehtf import create_app


class UserTestCase(TestCase):
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

    def test_create_user(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.post(
            f"/api/user?token={data.json['access_token']}",
            data={"username": "username2", "password": "password2"},
        )
        self.assertEqual(response.status_code, 201)

    def test_create_user_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        parameters = [
            ("", "password2", b"Username is required."),
            ("username2", "", b"Password is required."),
            ("test", "test", b"User already exists."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                username, password, message = parameter
                response = self.client.post(
                    f"/api/user?token={data.json['access_token']}",
                    data={"username": username, "password": password},
                )
                self.assertIn(message, response.data)

    def test_read_user(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/user/2?token={data.json['access_token']}")
        self.assertEqual(response.status_code, 200)

    def test_read_user_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/user/20?token={data.json['access_token']}")
        self.assertIn(b"User does not exist.", response.data)

    def test_update_user(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.put(
            f"/api/user/2?token={data.json['access_token']}",
            data={"username": "test_", "password": "test_", "role_id": 1},
        )
        self.assertEqual(response.status_code, 201)

    def test_update_user_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        parameters = [
            ("", "test_", 1, b"Username is required."),
            ("test_", "", 1, b"Password is required."),
            ("test_", "test_", "", b"Role ID is required."),
            ("test_", "", 1, b"Password is required."),
            ("admin", "test_", 1, b"User already exists."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                username, password, role_id, message = parameter
                response = self.client.put(
                    f"/api/user/2?token={data.json['access_token']}",
                    data={
                        "username": username,
                        "password": password,
                        "role_id": role_id,
                    },
                )
                self.assertIn(message, response.data)

    def test_delete_user(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(
            f"/api/user/2/delete?token={data.json['access_token']}"
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    main()
