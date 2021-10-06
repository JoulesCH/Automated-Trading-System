from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from datetime import date

load = html.Div([
    html.Div([
        html.H2('Para empezar ingresa un archivo con los datos o elige un símbolo:'),
        dbc.Row([
            dbc.Col(
                [
                html.H5("Subir un archivo:"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Agarra y arrastra o  ',
                        html.A('selecciona un archivo ')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px',
                        'margin-left':'auto',
                        'margin-right':'auto',
                        'margin-top':'0px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False,
                ),
                ]
            ),
            dbc.Col([
                html.H5("Descargar datos:"),
                dbc.FormGroup(
                    [
                        dbc.Label("Selecciona un stock symbol: ", html_for="symbol"),
                        dcc.Dropdown(
                                    id="symbol",
                                    options=[
                                        {"label": "AAPL - Apple, Inc.", "value": "AAPL"},
                                        {"label": "GOOGL - Alphabet, Inc.", "value": "GOOGL"},
                                        {"label": "TSLA - Tesla, Inc.", "value": "TSLA"},
                                        {"label": "AMZN - Amazon, Inc.", "value": "AMZN"},
                                        {"label": "BTC-USD - BITCOIN", "value": "BTC-USD"},
                                        {"label": "DOGE-USD - DOGECOIN", "value": "DOGE-USD"},
                                        {"label": "ETH-USD - ETHEREUM", "value": "ETH-USD"},

                                    ],
                                ),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Elige la frecuencia ", html_for="frequency"),
                                dcc.Dropdown(
                                    id="frequency",
                                    value = "1d",
                                    options=[
                                        # {"label": "M1", "value": "1m"},
                                        # {"label": "M5", "value": "5m"},
                                        # {"label": "M15", "value": "15m"},
                                        # {"label": "M30", "value": "30m"},
                                        {"label": "H1", "value": "1h"},
                                        {"label": "D1", "value": "1d"},
                                        {"label": "D5", "value": "5d"},
                                        {"label": "W1", "value": "1wk"},
                                        {"label": "MN", "value": "1mo"},
                                    ],
                                ) ,# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                            ]),
                            dbc.Col([
                                dbc.Label("Selecciona el rango de tiempo: ", html_for="date-picker"),
                                html.Br(),
                                dcc.DatePickerRange(
                                    id='date-picker',
                                    min_date_allowed=date(1995, 8, 5),
                                    max_date_allowed=date.today(),
                                    #initial_visible_month=date(2021, 2, 5),
                                    start_date = date(2021, 2, 5),
                                    end_date=date.today()
                                ),
                            ]),
                        ]),
                        dbc.Button("Cargar datos", id='goDownload', color="primary", className="mr-1", style = {'width':'100%'}),    
                    ]
                )
            ])
        ], style = {'margin-top':'30px'})
    ], id = 'uploadFile'),
    html.Div(
        dbc.Spinner(
            html.Div(id='output-data-upload'),
        color="primary"),
    style = {'margin-top':5})
])