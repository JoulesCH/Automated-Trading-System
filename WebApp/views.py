# Local packages
from core import app
from resources import Base, dash

#Installed packages
from dash import Dash
from dash_bootstrap_components import themes

app.route('/')(Base.home)

# Dash
appD = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/', 
    suppress_callback_exceptions=True, 
    update_title= None, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=0.8"}],
    external_stylesheets = [themes.BOOTSTRAP]
)

appD.layout = dash.layout
appD.title = 'Práctica 2 | EEDD'
import callbacks
app.route('/dash')(lambda: appD.index())


