# Built-in packages
import base64
import io

# Local packages
from views import appD

# Installed packages
from dash.dependencies import Input, Output, State
from dash import html
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


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
              Output('uploadFile', 'children'),
              Output('memory', 'data'),  
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(content, filename, last_modified):
    if not filename:
        raise PreventUpdate
    elif filename[-4:] not in ['.txt', '.csv']:
        return dbc.Alert("Tipo de archivo no permitido", color="danger"),
    else:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string).decode('utf-8').replace('\r','')
        try:
            listDecoded = [  float(value) for value in decoded.split('\n')]
        except:
            return dbc.Alert("Hay un dato no válido", color="danger"),

        fig = go.Figure(data = [go.Scatter(x=list(range(len(listDecoded))), y=listDecoded)])
        fig.add_trace(go.Scatter(x=list(range(len(listDecoded))), y=listDecoded, mode="markers") )
        fig.update_xaxes(rangeslider_visible=True)
        fig.layout.height = 700
        data = {
            'filename':filename,
            'last_modified':last_modified,
            'data':listDecoded
        }
        return html.Div([
            dcc.Graph(figure = fig, animate  =  True, id = 'tradeGraph'),
            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("Capital inicial:"),
                        dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = 2000.00),
                    ], style = {'width':'40%','margin-left':'auto', 'margin-right':'auto'}, id = 'formCapital'
                ),
                dbc.Button('¡Empezar a tradear!', color="primary", className="mr-1", id = 'beginButton'),
                ],
                style = {'text-align':'center'}
            )
        ]), html.Div([
                dbc.Alert([
                        html.H4("Datos cargados con éxito"),
                        html.Hr(),
                        "Revisa la gráfica y desliza hasta abajo para ingresar los datos faltantes", 
                    ], color="primary",duration=5000,
                )
        ]), data

@appD.callback(Output('tradeGraph', 'figure'), 
                Output('beginButton', 'children'),
                Output('formCapital', 'children'),
                Input("beginButton","n_clicks"),
                State('memory', 'data'))
def beginTrading(n, data):
    if not n:
        raise PreventUpdate
    else:
        response = requests.post('http://api:7071', {'data':data['data']}).json()
        
        
        return [go.Figure(data = [go.Scatter(x=list(range(len([1,2,3,4]))), y=[2,4,6,8])]), 
                html.A('Ingresar otro archivo', href = '/dash/',style = {'color':'white', 'text-decoration':'None'}), 
                None]