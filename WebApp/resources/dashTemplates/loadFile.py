from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

load = html.Div([
    html.Div([
        html.H2('Para empezar ingresa un archivo con los datos:'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Agarra y arrastra o  ',
                html.A('selecciona un archivo ')
            ]),
            style={
                'width': '70%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'margin-left':'auto',
                'margin-right':'auto',
                'margin-top':'30px'
            },
            # Allow multiple files to be uploaded
            multiple=False,
        ),
    ], id = 'uploadFile'),
    html.Div(
        dbc.Spinner(
            html.Div(id='output-data-upload'),
        color="primary"),
    style = {'margin-top':5})
])