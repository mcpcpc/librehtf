from dash import register_page
from dash_iconify import DashIconify
from dash_mantine_components import Container
from dash_mantine_components import Group
from dash_mantine_components import Button
from dash_mantine_components import PasswordInput
from dash_mantine_components import Text
from dash_mantine_components import TextInput
from dash_mantine_components import Stack

register_page(
    __name__,
    path="/login",
    title="Log In | LibreHTF",
    description="",
)

layout = Container(
    pt="xl",
    children=[
        Stack(
            spacing="lg",
            children=[
                TextInput(
                    id="username",
                    placeholder="Username",
                    icon=DashIconify(icon="bi:person"),
                ),
                PasswordInput(
                    id="password",
                    placeholder="Password",
                    icon=DashIconify(icon="bi:shield-lock"),
                ),
                Group(
                    position="right",
                    children=[
                        Button(
                            id="login",
                            children="Log In",
                        ),
                        Button(
                            id="back",
                            variant="transparent",
                            children="Back",
                        ),
                    ],
                )
            ]
        )
    ]
)