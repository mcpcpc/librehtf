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

def layout(device: str = None, test: str = None):
    return [
        Store(id="device", data=device),
        Grid(
            children=[
                Col(
                    span=3, 
                    id="device_tree",
                    children=None,
                ),
                Col(
                    span=3, 
                    id="test_tree",
                    children=None,
                ),
                Col(
                    span=9,
                    id="tasklist",
                ),
            ],
        ),
    ]


@callback(
    Output("device_tree", "children"),
    Input("device", "data"),
)
def update_navbar(device: str):
    rows = get_db().execute(
        "SELECT * FROM device"
    ).fetchall()
    if not rows:
        return no_update
    records = list(map(dict, rows))
    return [
        NavLink(
            label=r["name"],
            description=r["description"],
            href=f"/evaluate?device={r['id']}",
            active=device is str(r["id"]),
        ) for r in records
    ]


@callback(
    Output("test_tree", "children"),
    Input("device", "data"),
    Input("test", "data"),
)
def update_navbar(device: str, test: str):
    rows = get_db().execute(
        "SELECT * FROM test WHERE device_id = ?",
        (device,),
    ).fetchall()
    if not rows:
        return "No device selected"
    records = list(map(dict, rows))
    return [
        NavLink(
            label=r["name"],
            description=r["description"],
            href=f"/evaluate?device={device}&test={r['id']}",
            active=test is str(r["id"]),
        ) for r in records
    ]
