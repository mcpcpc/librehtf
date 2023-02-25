#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import register_page
from dash_mantine_components import Stack
from dash_mantine_components import Anchor
from dash_mantine_components import Text

register_page(__name__, path="/404")

layout = Stack(
    align="center",
    children=[
        Text(
            [
                "If you think this page should exist, create an issue ",
                Anchor(
                    "here",
                    underline=False,
                    href="#",
                ),
                ".",
            ]
        ),
        Anchor("Go back to home ->", href="/", underline=False),
    ],
)
