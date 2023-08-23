#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import callback
from dash import Input
from dash import no_update
from dash import Output
from dash import register_page
from dash import State
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

def layout(test: str = None):
    return [
        Store(id="test", data=test),
        Grid(
            gutter=0,
            children=[
                Col(
                    span=4,
                    children=[
                        Navbar(
                            id="navbar",
                            children=None,
                        ),
                    ],
                ),
                Col(
                    span=8,
                    id="tasklist",
                ),
            ],
        ),
    ]


@callback(
    Output("navbar", "children"),
    Input("navbar", "children"),
)
def update_navbar(children):
    rows = get_db().execute(
        """
        SELECT
            device.name AS device_name,
            device.description AS device_description,
            test.name AS test_name,
            test.description AS test_description,
            test.id AS test_id
        FROM test
            INNER JOIN device ON device.id = test.device_id
        """
    ).fetchall()
    if not rows:
        return no_update
    records = list(map(dict, rows))
    print(records)
    return [
        NavLink(
            label=r["name"],
            description=r["description"],
            noWrap=True,
        ) for r in records
    ]
