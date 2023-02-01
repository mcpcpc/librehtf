#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import main
from unittest import TestCase

from librehtf import create_app


class InitTestCase(TestCase):
    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app(
            {"TESTING": True, "DATABASE": self.db, "SECRET_KEY": "dev"}
        )
        self.runner = self.app.test_cli_runner()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_db_close(self):
        result = self.ctx.g.get("db")
        self.assertIsNone(result, result)

    def test_db_init_command(self):
        response = self.runner.invoke(args=["init-db"])
        self.assertIn("Initialized", response.output)


if __name__ == "__main__":
    main()
