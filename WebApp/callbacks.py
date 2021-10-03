# Built-in packages
import base64
import io
import statistics
from datetime import date
import os
import json
from random import choice
import string
import time

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
import yfinance as yf

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
              Input('goDownload', 'n_clicks'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State('symbol', 'value'),
              State('frequency', 'value'),
              State('date-picker', 'start_date'),
              State('date-picker', 'end_date'))
def update_output(content, n, filename, last_modified, symbol, frequency, start, end):
    print("***************************", start, end)
    if not filename:
        if not n:
            raise PreventUpdate
        elif not symbol or not frequency or not frequency or not start or not end :
            return dbc.Alert("Llena todos los datos", color="danger"), None, None
        else:
            listDecoded = yf.Ticker(symbol).history(period=frequency.lower(), start=start, end = end).Close.to_list()
        

    elif filename[-4:] not in ['.txt', '.csv']:
        return dbc.Alert("Tipo de archivo no permitido", color="danger"), None, None
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
        'data':listDecoded,
        'symbol': symbol  if symbol else filename[:filename.find('.')]
    }
    return html.Div([
            dcc.Graph(figure = fig, animate  =  True, id = 'tradeGraph'),
            html.Div([
                dbc.FormGroup(
                    [
                        dbc.Label("Capital inicial:"),
                        dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = 2000.00, id = 'Capital'),
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

def conect(data, capital, sma1, sma2):
    filename = ''.join(choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(10)) + '.txt'
    f = open(filename, "w")
    f.write(data.replace('*',' '))
    f.close()

    # Se ejecuta el programa 
    os.system(f"./main {filename} {capital}")
    time.sleep(1)

    # Se recolectan los datos
    with open(f"{filename}.json") as json_file:
        data = json.load(json_file)
    os.system(f"rm {filename}")
    os.system(f"rm {filename}.json")
    return  data

@appD.callback(Output('tradeGraph', 'figure'), 
                Output('beginButton', 'children'),
                Output('formCapital', 'children'),
                Output('tittle', 'children'),
                Input("beginButton","n_clicks"),
                State('memory', 'data'),
                State('Capital','value'))
def beginTrading(n, localMemory, Capital):
    if not n:
        raise PreventUpdate
    else:
        sma1 = 3
        sma2 = 10
        capital_ini = Capital
        
        #response = requests.post('http://127.0.0.1:5050/', {'data':'*'.join(str(x) for x in localMemory['data']), 'capital':capital_ini, 'sma1': sma1, 'sma2':sma2}).json()
        
        response = conect(**{'data':'*'.join(str(x) for x in localMemory['data']), 'capital':capital_ini, 'sma1': sma1, 'sma2':sma2})

        listDecoded = localMemory['data']

        fig = go.Figure()
        fig.layout.height = 700
        fig.update_xaxes(rangeslider_visible=True)
        
        df_stock = pd.DataFrame({'close':listDecoded})
        df_stock['SMA'] = df_stock.close.rolling(window = 20).mean()
        df_stock['stddev'] = df_stock.close.rolling(window = 20).std()
        df_stock['upper'] = df_stock.SMA + 2*df_stock.stddev
        df_stock['lower'] = df_stock.SMA - 2*df_stock.stddev

        #print(df_stock.iloc[19:30,:])
        fig.add_trace(go.Scatter(x = list(range(len(listDecoded))), y = df_stock.lower,mode = 'lines',  name = f'Lower',
                                    line = {'color': '#ff0000'}, fill = None ))
        fig.add_trace(go.Scatter(x = list(range(len(listDecoded))), y = df_stock.upper,mode = 'lines',  name = f'Upper',
                                    line = {'color': '#000000'} , fill='tonexty', fillcolor = 'rgba(255, 0, 0, 0.1)' ))
        
        fig.add_trace(go.Scatter(name='Datos Originales',x=list(range(len(listDecoded))), y=listDecoded, mode = 'lines+markers',  
                                line = {'color':'#636EFA'}))
        
        capital_final = response['capitalFinal']
        gain = response['gain']
        loss = response['loss']
        data = response['data']

        measures = ["absolute"]; x = ["Capital Inicial"]; y=[capital_ini-capital_ini]; text = ["Capital Inicial"]
        if not data:
            return [None,  
                'Actualizar capital', 
                [dbc.Label("Capital inicial:"),
                dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = 2000.00, id = 'Capital')],
                dbc.Alert("Capital insuficiente. Utiliza un capital que se iguale al precio ", color="danger")]
        for move in data:
            fig.add_trace(go.Scatter(x = [move['OpenIdx'], move['CloseIdx']], y= [move['OpenValue'], move['CloseValue']],
                                    name = move['Movimiento'],
                                    mode = 'lines+markers',
                                    marker_symbol = ['triangle-up', 'triangle-down'],
                                    marker_color = ['green', 'red'],
                                    marker_size=15,
                                    #line = 
                        ),
            )
            measures.append('relative')
            x.append(move['Movimiento'])
            y.append(move['Balance'])
            text.append(f'{move["Balance"]}')

        sma1List = []
        sma2List = []
        for idx in range(len(listDecoded)):
            sma1List.append(
                statistics.mean(listDecoded[idx:idx+sma1])
            )
            sma2List.append(
                statistics.mean(listDecoded[idx:idx+sma2])
            )

        fig.add_trace(go.Scatter(x = list(range(sma1, len(listDecoded))), y= sma1List,
                                    name = f'SMA_{sma1}',
                                    mode = 'lines',
                                    line = {'color': '#FF8A8A'}
                        ),
        )

        fig.add_trace(go.Scatter(x = list(range(sma2, len(listDecoded))), y= sma2List,
                                    name = f'SMA_{sma2}',
                                    mode = 'lines',
                                    line = {'color': '#949494'}
                        ),
        )
        measures.append('total')
        x.append('Capital Final')
        y.append(capital_final-capital_ini)
        text.append('Capital Final')
        df = pd.DataFrame(data)

        balances = []
        for value in df['Balance']:
            if not value: balances.append(html.P("", style = {'color':'red'}))
            elif value <= 0: balances.append(html.P(value, style = {'color':'red'}))
            else: balances.append(html.P(value, style  ={'color':'green'}))

        df['Balance'] = balances
        fig2 = make_subplots(
            rows=2, cols=2,
            vertical_spacing=0.1,
            specs=[[{'type':'domain'}, {'type':'domain'}],
                [{"type": "waterfall", "colspan": 2}, None],
            ]
        )
        fig2.add_trace(
            go.Waterfall(
                name = "20", orientation = "v",
                measure = measures,
                x = x,
                text = text,
                y =y,
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
                base = capital_ini
            ), row=2, col=1
        )
        labels = ["Gain", "Loss"]

        fig2.add_trace(go.Pie(labels=labels, values=[gain, loss], name="Gain vs Loss", hole=.9,
                                title = {"text": "<span style='font-size:0.7em;color:gray'>Gain vs Loss</span>"}
                            ),
                    1, 1)

        fig2.add_trace(go.Indicator(
                        mode = "number+delta",
                        value = capital_final,
                        title = {"text": "<span style='font-size:0.7em;color:gray'>Balance final</span>"},
                        delta = {'position': "bottom", 'reference': capital_ini, 'relative': False},
                        ),
                    1, 2)

        fig2.update_layout(
            showlegend=False,
            title_text="Datos relativos",
            autosize=True,
            height=500,
        )
        return [fig, 
                html.A('Ingresar otro archivo', href = '/dash/',style = {'color':'white', 'text-decoration':'None'}), 
                None, 
                html.Div([
                    html.H1('Resultados para ' + localMemory['symbol'], style = {'text-align':'center', 'margin-bottom':'30px'}),
                    dbc.Row(
                    [   
                        dbc.Col([
                            html.H2('Resumen'),
                            dcc.Graph(figure = fig2, config={'autosizable':True})
                        ]),
                        dbc.Col([
                            html.H2('Movimientos efectuados'), 
                            html.Div(
                                dbc.Table.from_dataframe(df, striped=True, 
                                                            responsive = True,
                                                            bordered=True, hover=True,
                                                            size = 'sm',
                                ),
                            style={'height': '500px', 'overflowY': 'auto'}                            
                            ),
                        ]),
                    ], style={'height':'500px','margin-bottom':'40px'}),
                    html.H2('Gráfica de movimientos', style={'margin-top':'20px'}),
                ])
                ]