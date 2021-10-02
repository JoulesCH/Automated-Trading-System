import os
import json
from random import choice
import string
import time

from flask_restful import Resource, abort 

from apiArgs import post_args

class Home(Resource):
    def get(self):
        return 'Hello world from API!', 200

    def post(self):
        args = post_args.parse_args()
        filename = ''.join(choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(10)) + '.txt'
        f = open(filename, "w")
        f.write(args["data"].replace('*',' '))
        f.close()
        
        # Se ejecuta el programa 
        os.system(f"./main {filename} {args['capital']}")
        time.sleep(1)

        # Se recolectan los datos
        with open(f"{filename}.json") as json_file:
            data = json.load(json_file)
        os.system(f"rm {filename}")
        os.system(f"rm {filename}.json")
        return  data