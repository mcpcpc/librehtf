#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import register_page
from dash_iconify import DashIconify
from dash_mantine_components import Stack
from dash_mantine_components import Text

register_page(__name__, path="/404")

layout = [
    Stack(
        align="center",
        p="xl",
        children=[
            DashIconify(icon="tabler:error-404", width=50),
            Text("This page does not exist."),
        ],
    )
]
