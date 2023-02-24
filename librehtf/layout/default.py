#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import clientside_callback
from dash import dcc
from dash import Input
from dash import Output
from dash import page_container
from dash import State
from dash_iconify import DashIconify
from dash_mantine_components import ActionIcon
from dash_mantine_components import Anchor
from dash_mantine_components import Button
from dash_mantine_components import Container
from dash_mantine_components import Group
from dash_mantine_components import Header
from dash_mantine_components import MantineProvider
from dash_mantine_components import NotificationsProvider

header = Header(
    height=57,
    fixed=True,
    py="md",
    px="xl",
    children=[
        Group(
            position="apart",
            align="flex-start",
            children=[
                Group(
                    children=[
                        Anchor(
                            Button(
                                id="home",
                                variant="subtle",
                                children="LibreHTF",
                                compact=True,
                                leftIcon=DashIconify(icon="game-icons:feather-wound"),
                            ),
                            href="/",
                        ),
                        Anchor(
                            Button(
                                id="evaluate",
                                variant="light",
                                children="Evaluate",
                                compact=True,
                            ),
                            href="/evaluate",
                        ),
                        Anchor(
                            Button(
                                id="manage",
                                variant="light",
                                children="Manage",
                                compact=True,
                            ),
                            href="/manage",
                        ),
                    ]
                ),
                Group(
                    children=[
                        ActionIcon(
                            id="color-scheme-toggle",
                            variant="transparent",
                            children=DashIconify(icon="radix-icons:blending-mode"),
                        ),
                    ]
                ),
            ]
        ),
    ]
)

wrapper = Container(
    id="wrapper",
    my=57,
    children=page_container,
)


def layout(data):
    return MantineProvider(
        id="theme-provider",
        theme={"colorScheme": "light"},
        withGlobalStyles=True,
        withNormalizeCSS=True,
        children=[
            MantineProvider(
                theme={
                    "primaryColor": "grape",
                    "fontFamily": "system-ui, sans-serif",
                },
                inherit=True,
                children=[
                    dcc.Store(id="theme-store", storage_type="local"),
                    NotificationsProvider(children=[header, wrapper]),
                ],
            )
        ],
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