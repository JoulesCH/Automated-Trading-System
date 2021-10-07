"""Main application package"""

##### Installed packages
from flask import Flask
##### Build-in packages
from os import environ

##### Local
from . import config
app = Flask(__name__, template_folder='../templates')

environment = environ.get("FLASK_ENV", default="development")
if environment == "development":
   print('\n\nTHIS IS A DEVELOPMENT ENVIRONMENT \n\n')
   cfg = config.DevelopmentConfig()
elif environment == "production":
   print('\n\nTHIS IS A PRODUCTION ENVIRONMENT\n\n')
   cfg = config.ProductionConfig()
 
app.config.from_object(cfg)

import views