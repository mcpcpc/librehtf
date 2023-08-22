#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import callback
from dash import Input
from dasg import Output
from dash import register_page
from dash_iconify import DashIconify
from dash_mantine_components import Accordion
from dash_mantine_components import AccordionItem
from dash_mantine_components import AccordionControl
from dash_mantine_components import AccordionPanel
from dash_mantine_components import Stack
from dash_mantine_components import Text
from dash_mantine_components import Title

register_page(__name__, path="/evaluate")

layout = [
    Stack(
        children=[
            Title("Evaluate"),
            Text(""),
        ]
    ),
    Accordion(id="accordion"),
]