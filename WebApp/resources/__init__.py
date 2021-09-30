# Installed packages
import requests
from flask import redirect, render_template

class Base:
    def home():
        #response = requests.get('http://api:7071')
        # Create a cookie
        return redirect('/dash')
