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
from dash_mantine_components import Group
from dash_mantine_components import Navbar
from dash_mantine_components import NavLink
from dash_mantine_components import Stack
from dash_mantine_components import Text

from librehtf.db import get_db
from librehtf.utils.plugin import MeasurementPlugin

register_page(__name__, path_template="/eval/<device_id>")

def layout(device_id: str = None, test_id: str = None):
    return [
        Store(id="device_id", data=device_id),
        Store(id="test_id", data=test_id),
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
                    id="tasks",
                    children=[],
                ),
            ],
        ),
    ]


@callback(
    Output("navbar", "children"),
    Input("device_id", "data"),
)
def update_navbar(device_id):
    rows = get_db().execute(
        "SELECT * FROM test WHERE device_id = ?",
        (device_id,),
    ).fetchall()
    if not rows:
        return no_update
    records = list(map(dict, rows))
    return [
        NavLink(
            label=record["name"],
            description=record["description"],
            noWrap=True,
            rightSection=DashIconify(
                icon="ic:baseline-chevron-right",
            ),
            href=f"/eval/{device_id}?test_id={record['id']}",
        ) for record in records
    ]


@callback(
    Output("tasks", "children"),
    Input("test_id", "data"),
)
def update_stepper(test_id):
    rows = get_db().execute(
        "SELECT * FROM task WHERE test_id = ?",
        (test_id,),
    ).fetchall()
    if not rows:
        return no_update
    records = list(map(dict, rows))
    return [
        Group(
            p="lg",
            children=[
                Stack(
                    children=[
                        Text(record["name"]),
                        Text(
                            f"{record['reference']}",
                            size="sm",
                            color="dimmed",
                        ),
                    ]
                ),
            ]
        ) for record in records
    ]
