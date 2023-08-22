#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import callback
from dash import Input
from dash import no_update
from dash import Output
from dash import register_page
from dash_iconify import DashIconify
from dash.dcc import Store
from dash_mantine_components import Col
from dash_mantine_components import Grid
from dash_mantine_components import Card
from dash_mantine_components import Navbar
from dash_mantine_components import NavLink

from librehtf.db import get_db
from librehtf.utils.plugin import MeasurementPlugin

register_page(__name__, path="/evaluate")

def layout(test: str = None, **parameters):
    return [
        Store(id="test", data=test),
        Grid(
            children=[
                Col(
                    span=3,
                    children=[
                        Navbar(
                            id="navbar",
                            children=None,
                        ),
                    ],
                ),
                Col(
                    span=9,
                    id="tasklist",
                ),
            ],
        ),
    ]

@callback(
    Output("navbar", "children"),
    Input("test", "data"),
)
def update_navbar(test: str):
    rows = get_db().execute(
        "SELECT * FROM test"
    ).fetchall()
    if not rows:
        return no_update
    records = list(map(dict, rows))
    return [
        NavLink(
            label=r["name"],
            description=r["name"],
        ) for r in records
    ]