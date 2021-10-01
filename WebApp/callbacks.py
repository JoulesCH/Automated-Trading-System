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
from plotly.subplots import make_subplots

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

        fig = go.Figure(data = [go.Scatter(x=list(range(len(listDecoded))), y=listDecoded, mode = 'lines+markers')])
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
                Output('tittle', 'children'),
                Input("beginButton","n_clicks"),
                State('memory', 'data'))
def beginTrading(n, data):
    if not n:
        raise PreventUpdate
    else:
        #response = requests.post('http://api:7071', {'data':data['data']}).json()
        listDecoded = data['data']
        fig = go.Figure(data = [go.Scatter(name='Datos Originales',x=list(range(len(listDecoded))), y=listDecoded, mode = 'lines+markers')])
        fig.layout.height = 700
        fig.update_xaxes(rangeslider_visible=True)
        capital_ini = 2000
        data = [
            {'Movimiento': '123a','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':500},
            {'Movimiento': '123b','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
            {'Movimiento': '123c','Volumen':3, 'OpenValue':1143.45, 'OpenIdx':26, 'CloseValue':1200.05,'CloseIdx':103, 'Balance':500},
            {'Movimiento': '123d','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
            {'Movimiento': '123e','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':-500},
            {'Movimiento': '123f','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':-500},
            {'Movimiento': '123g','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
            {'Movimiento': '123h','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':500},
            {'Movimiento': '123i','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
            {'Movimiento': '123j','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':-500},
            {'Movimiento': '123k','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
        ]
        measures = ["absolute"]; x = ["Capital"]; y=[capital_ini]; text = ["Capital"]
        for move in data:
            fig.add_trace(go.Scatter(x = [move['OpenIdx'], move['CloseIdx']], y= [move['OpenValue'], move['CloseValue']],
                name = move['Movimiento'],
                mode = 'lines+markers') 
            )
            measures.append('relative')
            x.append(move['Movimiento'])
            y.append(move['Balance'])
            text.append(f'{move["Balance"]}')
        df = pd.DataFrame(data)
        balances = []
        for value in df['Balance']:
            if value <= 0: balances.append(html.P(value, style = {'color':'red'}))
            else: balances.append(html.P(value, style  ={'color':'green'}))

        df['Balance'] = balances
        fig2 = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            specs=[[{"type": "waterfall"}],
                [{"type": "scatter"}],
            ]
        )
        fig2.add_trace(
            go.Waterfall(
                name = "20", orientation = "v",
                measure = measures,
                x = x,
                #textposition = "outside",
                text = text,
                y =y,
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ), row=1, col=1
        )
        return [fig, 
                html.A('Ingresar otro archivo', href = '/dash/',style = {'color':'white', 'text-decoration':'None'}), 
                None, 
                html.Div([
                    dbc.Row(
                    [   dbc.Col([
                            html.H2('Movimientos efectuados'), 
                            html.Div(
                                dbc.Table.from_dataframe(df, striped=True, 
                                                            responsive = True,
                                                            bordered=True, hover=True,
                                                            size = 'sm',
                                ),
                            style={'height': '300px', 'overflowY': 'auto'}                            
                            ),
                        ]),
                        dbc.Col([
                            html.H2('Resumen'),
                            dcc.Graph(figure = fig2)
                        ]),
                    ]),
                    html.H2('Gráfica de movimientos'),
                ])
                ]