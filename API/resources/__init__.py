from flask_restful import Resource, abort 

class Home(Resource):
    def get(self):
        return 'Hello world from API!', 200