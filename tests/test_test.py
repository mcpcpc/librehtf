#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from librehtf import create_app


class TestTestCase(TestCase):
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

    def test_create_test(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.post(
            f"/api/test?token={data.json['access_token']}",
            data={"name": "name3", "description": "description3", "device_id": 1},
        )
        self.assertEqual(response.status_code, 201)

    def test_create_test_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        parameters = [
            ("", "description2", 1, b"Name is required."),
            ("name2", "", 1, b"Description is required."),
            ("name2", "description2", "", b"Device ID is required."),
            ("name1", "description1", 1, b"Test already exists or device ID invalid."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, device_id, message = parameter
                response = self.client.post(
                    f"/api/test?token={data.json['access_token']}",
                    data={
                        "name": name,
                        "description": description,
                        "device_id": device_id,
                    },
                )
                self.assertIn(message, response.data)

    def test_read_test(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/test/1?token={data.json['access_token']}")
        self.assertEqual(response.status_code, 200)

    def test_read_test_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/test/3?token={data.json['access_token']}")
        self.assertIn(b"Test does not exist.", response.data)

    def test_update_test(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.put(
            f"/api/test/1?token={data.json['access_token']}",
            data={"name": "name1_", "description": "description1_", "device_id": 1},
        )
        self.assertEqual(response.status_code, 201)

    def test_update_test_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        parameters = [
            ("", "description2_", 1, b"Name is required."),
            ("name2_", "", 1, b"Description is required."),
            ("name2_", "description2_", "", b"Device ID is required."),
            ("name1", "description1", 1, b"Test already exists or device ID invalid."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, device_id, message = parameter
                response = self.client.put(
                    f"/api/test/2?token={data.json['access_token']}",
                    data={
                        "name": name,
                        "description": description,
                        "device_id": device_id,
                    },
                )
                self.assertIn(message, response.data)

    def test_delete_test(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(
            f"/api/test/1/delete?token={data.json['access_token']}"
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    main()
