# Built-in packages
import base64
import io

# Local packages
from views import appD

# Installed packages
from dash.dependencies import Input, Output, State
from dash import html
#from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc

@appD.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@appD.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(content, filename, last_modified):
    if not filename:
        return None
    elif filename[-4:] not in ['.txt', '.csv']:
        return html.P('Tipo de archivo no permitido', style = {'color':'red'})
    else:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8').replace('\r','')
        try:
            listDecoded = [  float(value) for value in decoded.split('\n')]
        except:
            return html.P('Hay un dato no válido', style = {'color':'red'})

        df = pd.Series(listDecoded)
        fig = go.Figure(data = [go.Scatter(x=list(range(len(listDecoded))), y=listDecoded)])
        fig.add_trace(go.Scatter(x=list(range(len(listDecoded))), y=listDecoded, mode="markers") )
        fig.update_xaxes(rangeslider_visible=True)
        return html.Div([
            dcc.Graph(figure = fig, animate  =  True),
            html.Div(
                dbc.Button('¡Empezar a tradear!', color="primary", className="mr-1"),
                style = {'text-align':'center'}
            )
        ])
    