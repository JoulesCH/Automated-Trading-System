import requests

class Base:
    def home():
        response = requests.get('http://0.0.0.0:7070')
        return f'Hola mundo! {response.status_code}'