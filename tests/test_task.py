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

    def test_create_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.post(
            f"/api/task?token={data.json['access_token']}",
            data={"name": "name2", "command": "command2", "test_id": 1, "operation_id": 1, "datatype_id": 1}
        )
        self.assertEqual(response.status_code, 201)

    def test_create_task_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        self.client.post(
            f"/api/task?token={data.json['access_token']}",
            data={"name": "name2", "command": "command2", "test_id": 1, "operation_id": 1, "datatype_id": 1}
        )
        parameters = [
            ("", "command2", 1, b"Name is required."),
            ("name2", "", 1, 1, 1, b"Command is required."),
            ("name2", "command2", "", 1, 1, b"Test ID is required."),
            ("name2", "command2", 1, "", 1, b"Operation ID is required."),
            ("name2", "command2", 1, 1, "", b"Datatype ID is required."),
            ("name1", "command1", 1, 1, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 9, 1, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 1, 9, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 1, 1, 9, b"Task already exists or test, operation or datatype ID invalid."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, device_id, operation_id, datatype_id, message = parameter
                response = self.client.post(
                    f"/api/task?token={data.json['access_token']}",
                    data={
                      "name": name,
                      "description": description,
                      "device_id": device_id,
                      "operation_id": operation_id,
                      "datatype_id": datatype_id
                    }
                )
                self.assertIn(message, response.data)

    def test_read_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/task/1?token={data.json['access_token']}")
        self.assertEqual(response.status_code, 200)


    def test_read_task_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/task/2?token={data.json['access_token']}")
        self.assertIn(b"Task does not exist.", response.data)

    def test_update_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.put(
            f"/api/task/1?token={data.json['access_token']}",
            data={"name": "name1_", "command": "command1_", "test_id": 1, "operation_id": 1, "datatype_id": 1}
        )
        self.assertEqual(response.status_code, 201)

    def test_update_task_errors(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        self.client.post(
            f"/api/task?token={data.json['access_token']}",
            data={"name": "name2", "command": "command2", "test_id": 1, "operation_id": 1, "datatype_id": 1}
        )
        parameters = [
            ("", "command2", 1, b"Name is required."),
            ("name2", "", 1, 1, 1, b"Command is required."),
            ("name2", "command2", "", 1, 1, b"Test ID is required."),
            ("name2", "command2", 1, "", 1, b"Operation ID is required."),
            ("name2", "command2", 1, 1, "", b"Datatype ID is required."),
            ("name1", "command1", 1, 1, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 9, 1, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 1, 9, 1, b"Task already exists or test, operation or datatype ID invalid."),
            ("name1", "command1", 1, 1, 9, b"Task already exists or test, operation or datatype ID invalid."),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, device_id, operation_id, datatype_id, message = parameter
                response = self.client.put(
                    f"/api/task/2?token={data.json['access_token']}",
                    data={
                      "name": name,
                      "description": description,
                      "device_id": device_id,
                      "operation_id": operation_id,
                      "datatype_id": datatype_id
                    }
                )
                self.assertIn(message, response.data)

    def test_delete_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/auth/token", data={"expires_in": 600})
        response = self.client.get(f"/api/task/1/delete?token={data.json['access_token']}")
        self.assertEqual(response.status_code, 200)
