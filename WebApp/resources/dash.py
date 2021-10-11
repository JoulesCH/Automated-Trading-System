# Installed pacakges
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
# Local packages
from .dashTemplates import navbar, loadFile

LAYOUT = html.Div([
    dcc.Store(id='memory'),
    dcc.Location(id='url', refresh=False),
    navbar.navbar,
    
    html.Div([
        html.Div([
            html.Div(id = 'tittle'),
            loadFile.load,

        ], style = {'margin':30}),
        
        dbc.Navbar(id='Results', color="dark",
                        dark=True,
                        style = {'background-color':'#ffffff', "flex-flow":"wrap"},
                        sticky = "bottom",
                        fixed = "bottom",
                        className = 'navB')

    ], id = 'principalLaout'),
], style = {'background-color':'#001F40', 'color':'#e3e3e3', 'padding-bottom':'500px'})#
    
##a2adb2 

#3E3F58