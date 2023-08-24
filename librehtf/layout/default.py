#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import callback
from dash import clientside_callback
from dash import Input
from dash import Output
from dash import page_container
from dash import page_registry
from dash import State
from dash.dcc import Location
from dash.dcc import Store
from dash_iconify import DashIconify
from dash_mantine_components import ActionIcon
from dash_mantine_components import Group
from dash_mantine_components import Header
from dash_mantine_components import Container
from dash_mantine_components import MantineProvider
from dash_mantine_components import Notifications
from dash_mantine_components import Select
from dash_mantine_components import Text

from librehtf.db import get_db

header = Header(
    height=70,
    p="md",
    fixed=True,
    children=[
        Group(
            position="apart",
            children=[
                Text("LibreHTF"),
                Group(
                    children=[
                        Select(
                            id="select",
                            clearable=True,
                            nothingFound="No match found",
                            placeholder="Search",
                            searchable=True,
                        ),
                        ActionIcon(
                            id="color-scheme-toggle",
                            variant="transparent",
                            children=[
                                DashIconify(
                                    icon="radix-icons:blending-mode",
                                ),
                            ],
                        ),
                    ],
                ),
            ], 
        ),
    ],
)

wrapper = Container(
    fluid=True,
    pt=70,
    px="0px",
    children=page_container,
)

layout = MantineProvider(
    id="theme-provider",
    theme={"colorScheme": "light"},
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        MantineProvider(
            theme={
                "primaryColor": "indigo",
                "fontFamily": "'Open Sans', verdana, arial, sans-serif",
            },
            inherit=True,
            children=[
                Store(id="theme-store", storage_type="local"),
                Location(id="location"),
                Notifications(id="notifications"),
                header,
                wrapper,
            ],
        ),
    ],
)

clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("location", "pathname"),
    Input("select", "value"),
)

clientside_callback(
    """ function(data) { return data } """,
    Output("theme-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    """function(n_clicks, data) {
        if (data) {
            if (n_clicks) {
                const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                return { colorScheme: scheme } 
            }
            return dash_clientside.no_update
        } else {
            return { colorScheme: "light" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)


@callback(
    Output("select", "data"),
    Input("select", "data"),
)
def update_select(data):
    rows = get_db().execute(
        "SELECT * FROM device"
    ).fetchall()
    if not rows:
        return None
    records = list(map(dict, rows))
    return [
        {
            "label": record["name"],
            "value": record["id"],
        } for record in records
    ]
