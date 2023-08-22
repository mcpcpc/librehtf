#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import callback
from dash import Input
from dash import no_update
from dash import Output
from dash import register_page
from dash_iconify import DashIconify
from dash_mantine_components import Stack
from dash_mantine_components import Text
from dash_mantine_components import Title

from librehtf.utils.plugin import MeasurementPlugin

register_page(__name__, path="/evaluate/<device>")

def layout(device: str = None):
    return [
        Stack(
            p="xl",
            children=[
                Title("Evaluate"),
                Text(""),
            ]
        ),
    ]
