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
import subprocess

# Local packages
from views import appD

# Installed packages
import dash
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
    fig.update_layout(template='plotly_dark', paper_bgcolor="#001F40", plot_bgcolor = "#000F20")
    data = {
        'filename':filename,
        'last_modified':last_modified,
        'data':listDecoded,
        'symbol': symbol  if symbol else filename[:filename.find('.')]
    }
    return html.Div([
            html.H2(symbol  if symbol else filename[:filename.find('.')], style = {'margin-bottom':'40px'}),
            html.Div([
                dcc.Graph(figure = fig, animate  =  True, id = 'tradeGraph'),
            ], id = 'grafico1'),
            html.Div([
                html.Div([
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H2(
                                dbc.Button(
                                    f"¿No estás seguro de los parámetros? Da clic y abre el glosario",
                                    color="link",
                                    id=f"group-1-toggle",
                                    n_clicks=0,
                                )
                            )
                        ),
                        dbc.Collapse(
                            dbc.CardBody([
                                html.Ul([
                                    html.Li([html.B("Precisión"), ": Representa el margen de error con el que se decide si un punto es de soporte o de resistencia"]),
                                    html.Li([html.B("Máximo de inversión"), ": Indica el monto máximo que se puede invertir, es relativo al capital disponible"]),
                                    html.Li([html.B("Stop Loss"), ": La posición se cerrará cuando se haya perdido esta cantidad"]),
                                    html.Li([html.B("Take Profit"), ": Cuando la ganancia sea igual al precio de apertura multiplicado por este parámetro, entonces se cerrará la posición"]),
                                ])
                            ]),
                            id=f"collapse-1",
                            is_open=False,
                        ),
                    ]
                ),

                ], className="accordion", style = {'text-align':'left','color':'black','width':'70%','margin-left':'auto', 'margin-right':'auto', 'margin-bottom':'30px'}),

                dbc.FormGroup(
                    [   
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Capital inicial:"),
                                dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = 2000.00, id = 'Capital'),
                            ]),
                            dbc.Col([
                                dbc.Label("Precisión:"),
                                dbc.Input(placeholder="ERROR", type="number", min = 0, value = 0.006, id = 'ERROR'),
                            ]),
                            dbc.Col([
                                dbc.Label("Máximo de inversión relativo:"),
                                dbc.Input(placeholder="MAX_INV", type="number", min = 0, value = 0.8, id = 'MAX_INV'),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Stop Loss absoluto:"),
                                dbc.Input(placeholder="STOP_LOSS", type="number", min = 0, value = 10000, id = 'STOP_LOSS'),
                            ]),
                            dbc.Col([
                                dbc.Label("Take Profit relativo:"),
                                dbc.Input(placeholder="TAKE_PROFIT", type="number", min = 1, value = 1.02, id = 'TAKE_PROFIT'),
                            ]),
                        ])

                    ], style = {'width':'70%','margin-left':'auto', 'margin-right':'auto'}, id = 'formCapital'
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


i = 1
@appD.callback(
    Output(f"collapse-{i}", "is_open") ,
    Input(f"group-{i}-toggle", "n_clicks"),
    State(f"collapse-{i}", "is_open"),
)
def toggle_accordion(n1, is_open1):
    if n1:
        return not is_open1
    return is_open1

def conect(data, capital, sma1, sma2, ERROR, MAX_INV, STOP_LOSS, TAKE_PROFIT):
    filename = ''.join(choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(10)) + '.txt'
    # f = open(filename, "w")
    # f.write(data.replace('*',' '))
    # f.close()

    # Se ejecuta el programa 
    # os.system(f"./main {filename} {capital}")
    # time.sleep(1)
    parametros = [str(ERROR), str(MAX_INV), str(STOP_LOSS), str(TAKE_PROFIT)]

    stdOutput = os.popen(f'./main {filename} {capital} {" ".join(parametros)} {data.replace("*", " ")}').read() 
    #print(stdOutput, stdOutput[stdOutput.find('{'):])
    stdOutput = stdOutput[stdOutput.find('{'):]
    print('\n\n\n','*'*25, stdOutput, '*'*25,'\n\n\n' )
    if not stdOutput:
        return None
    data = json.loads(stdOutput)
    # Se recolectan los datos
    # with open(f"{filename}.json") as json_file:
    #     data = json.load(json_file)
    # os.system(f"rm {filename}")
    # os.system(f"rm {filename}.json")
    return  data

@appD.callback(Output('grafico1', 'children'), 
                Output('beginButton', 'children'),
                Output('formCapital', 'children'),
                Output('tittle', 'children'),
                Output('Results', 'children'),
                Input("beginButton","n_clicks"),
                State('memory', 'data'),
                State('Capital','value'),
                State('ERROR','value'),
                State('MAX_INV','value'),
                State('STOP_LOSS','value'),
                State('TAKE_PROFIT','value'),
                )
def beginTrading(n, localMemory, Capital, ERROR, MAX_INV, STOP_LOSS, TAKE_PROFIT):
    if not n:
        raise PreventUpdate
    else:
        sma1 = 3
        sma2 = 10
        capital_ini = Capital
        
        #response = requests.post('http://127.0.0.1:5050/', {'data':'*'.join(str(x) for x in localMemory['data']), 'capital':capital_ini, 'sma1': sma1, 'sma2':sma2}).json()
        
        response = conect(ERROR = ERROR, MAX_INV = MAX_INV, STOP_LOSS =  STOP_LOSS, TAKE_PROFIT = TAKE_PROFIT,
                            **{   'data':'*'.join(str(x) for x in localMemory['data']), 
                                'capital':capital_ini, 
                                'sma1': sma1, 
                                'sma2':sma2,
                                })
        if not response:
            return [None,  
                'Actualizar capital', 
                [dbc.FormGroup(
                        [   
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Capital inicial:"),
                                    dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = Capital, id = 'Capital'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Precisión:"),
                                    dbc.Input(placeholder="ERROR", type="number", min = 0, value = ERROR, id = 'ERROR'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Máximo de inversión relativo:"),
                                    dbc.Input(placeholder="MAX_INV", type="number", min = 0, value = MAX_INV, id = 'MAX_INV'),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Stop Loss absoluto:"),
                                    dbc.Input(placeholder="STOP_LOSS", type="number", min = 0, value = STOP_LOSS, id = 'STOP_LOSS'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Take Profit relativo:"),
                                    dbc.Input(placeholder="TAKE_PROFIT", type="number", min = 1, value = TAKE_PROFIT, id = 'TAKE_PROFIT'),
                                ]),
                            ])

                        ], style = {'width':'70%','margin-left':'auto', 'margin-right':'auto'}, id = 'formCapital'
                    ),  ],
                dbc.Alert("Capital insuficiente. Utiliza un capital que se iguale al precio ", color="danger"), None]
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
                                    line = {'color': '#ffffff'} , fill='tonexty', fillcolor = 'rgba(255, 255, 255, 0.1)' ))
        
        fig.add_trace(go.Scatter(name='Datos Originales',x=list(range(len(listDecoded))), y=listDecoded, mode = 'lines+markers',  
                                line = {'color':'#636EFA'}))
        
        capital_final = response['capitalFinal']
        gain = response['gain']
        loss = response['loss']
        data = response['data']
        if not data:
            return [None,  
                'Actualizar capital', 
                [dbc.FormGroup(
                        [   
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Capital inicial:"),
                                    dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = Capital, id = 'Capital'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Precisión:"),
                                    dbc.Input(placeholder="ERROR", type="number", min = 0, value = ERROR, id = 'ERROR'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Máximo de inversión relativo:"),
                                    dbc.Input(placeholder="MAX_INV", type="number", min = 0, value = MAX_INV, id = 'MAX_INV'),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Stop Loss absoluto:"),
                                    dbc.Input(placeholder="STOP_LOSS", type="number", min = 0, value = STOP_LOSS, id = 'STOP_LOSS'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Take Profit relativo:"),
                                    dbc.Input(placeholder="TAKE_PROFIT", type="number", min = 1, value = TAKE_PROFIT, id = 'TAKE_PROFIT'),
                                ]),
                            ])

                        ], style = {'width':'70%','margin-left':'auto', 'margin-right':'auto'}, id = 'formCapital'
                    ),  ],
                dbc.Alert("Capital insuficiente. Utiliza un capital que se iguale al precio ", color="danger"), None]
        measures = ["absolute"]; x = ["Capital Inicial"]; y=[capital_ini-capital_ini]; text = ["Capital Inicial"]
        
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
            #title_text="Datos relativos",
            #autosize=True,
            #height=500,
        )
        
        fig.update_layout(template='plotly_dark', paper_bgcolor="#001F40", plot_bgcolor = "#000F20", margin=dict(l=5, r=5, t=5, b=5),
            showlegend=False,)
        
        fig2.update_layout(template='plotly_dark', paper_bgcolor="#001F40", plot_bgcolor = "#000F20", margin=dict(l=5, r=5, t=5, b=5))
        return [None, 
                "Modificar parámetros", 
                None, 
                html.Div([
                    html.H1('Resultados para ' + localMemory['symbol'], style = {'text-align':'center', 'margin-bottom':'30px'}),
                    html.H2('Resumen'),
                    dcc.Graph(figure = fig2, config={'autosizable':True}),
                   
                    html.H2('Movimientos efectuados:'),
                    dbc.Row([
                        dbc.Col([ 
                            html.Div(
                                dbc.Table.from_dataframe(df, striped=True, 
                                                            responsive = True,
                                                            bordered=True, hover=True,
                                                            size = 'sm',
                                                            dark=True,
                                ),
                            style={'height': '700px', 'overflowY': 'auto', 'margin-top':'50px', 'padding':'0px'},
                            className = 'tableHG'                            
                            ),
                        ], width=5, style = {'padding-right':'5px'}),
                        dbc.Col([                    
                            dcc.Graph(figure = fig, animate  =  True, style = {'padding':'0px'}),
                        ], width=7, style = {'padding':'0px'}),
                    ]),
                    html.H2('Parámetros ingresados:'),
                    html.P("Modifica los parámetros y da clic al botón"),
                    dbc.FormGroup(
                        [   
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Capital inicial:"),
                                    dbc.Input(placeholder="Valor entero mayor a 0", type="number", min = 0, value = Capital, id = 'Capital'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Precisión:"),
                                    dbc.Input(placeholder="ERROR", type="number", min = 0, value = ERROR, id = 'ERROR'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Máximo de inversión relativo:"),
                                    dbc.Input(placeholder="MAX_INV", type="number", min = 0, value = MAX_INV, id = 'MAX_INV'),
                                ]),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Stop Loss absoluto:"),
                                    dbc.Input(placeholder="STOP_LOSS", type="number", min = 0, value = STOP_LOSS, id = 'STOP_LOSS'),
                                ]),
                                dbc.Col([
                                    dbc.Label("Take Profit relativo:"),
                                    dbc.Input(placeholder="TAKE_PROFIT", type="number", min = 1, value = TAKE_PROFIT, id = 'TAKE_PROFIT'),
                                ]),
                            ])

                        ], style = {'width':'70%','margin-left':'auto', 'margin-right':'auto'}, id = 'formCapital'
                    ),    
                
                ]),
                [
                    dbc.Row([
                        dbc.Col(f'Capital: {capital_final}', width=2),
                        dbc.Col(f'Balance: {Capital}', width=2),
                        dbc.Col(f'Margen: {capital_final-capital_ini}', width=2),
                        dbc.Col(f'Margen Libre: {Capital}%', width=2),
                        dbc.Col(f'Beneficio: {Capital}', width=2),
                    ], justify="center",)
                ],
                        
                ]
from resources.dashTemplates import paths

base = '/dash/'
paths = {
    base+'mt':paths.marco_teorico,
    base+'d': paths.diagrama,
    base+'r':paths.repositorio,
    base+'p':paths.pruebas,
    base+'c':paths.conclusiones  
}

@appD.callback(Output('principalLaout', 'children'),
                Input('url', 'pathname'))
def updatePrincipalLayout(pathname):
    print(pathname)
    if pathname == '/dash/' or pathname not in paths:
        raise PreventUpdate
    return paths[pathname]