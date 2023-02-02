#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from librehtf import create_app


class DeviceTestCase(TestCase):
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

    def test_create_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.post(
            f"/api/device?token={data.json['access_token']}",
            data={"name": "name2", "description": "description2"},
        )
        self.assertEqual(response.status_code, 201)

    def test_create_device_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        parameters = [
            ("", "description2", b"Name is required."),
            ("name2", "", b"Description is required."),
            ("name1", "description1", b"Device already exists."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, message = parameter
                response = self.client.post(
                    f"/api/device?token={data.json['access_token']}",
                    data={"name": name, "description": description},
                )
                self.assertIn(message, response.data)

    def test_read_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/device/1?token={data.json['access_token']}")
        self.assertEqual(response.status_code, 200)

    def test_read_device_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/device/2?token={data.json['access_token']}")
        self.assertIn(b"Device does not exist.", response.data)

    def test_update_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.put(
            f"/api/device/1?token={data.json['access_token']}",
            data={"name": "name1_", "description": "description1_"},
        )
        self.assertEqual(response.status_code, 201)

    def test_update_device_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        self.client.post(
            f"/api/device?token={data.json['access_token']}",
            data={"name": "name2", "description": "description2"},
        )
        parameters = [
            ("", "description2_", b"Name is required."),
            ("name2_", "", b"Description is required."),
            ("name1", "description1", b"Device already exists."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, message = parameter
                response = self.client.put(
                    f"/api/device/2?token={data.json['access_token']}",
                    data={"name": name, "description": description},
                )
                self.assertIn(message, response.data)

    def test_delete_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(
            f"/api/device/1/delete?token={data.json['access_token']}"
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    main()
