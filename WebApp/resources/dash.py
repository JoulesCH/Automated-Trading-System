# Installed pacakges
from dash import dcc
from dash import html

# Local packages
from .dashTemplates import navbar, loadFile

layout = html.Div([
    navbar.navbar,
    html.Div([
        loadFile.load,
    ], style = {'margin':30})
])