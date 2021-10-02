import os
import json
from random import choice
import string

from flask_restful import Resource, abort 

from apiArgs import post_args

class Home(Resource):
    def get(self):
        return 'Hello world from API!', 200

    def post(self):
        args = post_args.parse_args()
        filename = ''.join(choice(string.ascii_lowercase + string.ascii_uppercase) for _ in range(10)) + '.txt'
        f = open(filename, "w")
        f.write(args["data"].replace('*','\n'))
        f.close()
        
        # Se ejecuta el programa 
        #os.system(f"./main_unix {filename}")

        # Se recolectan los datos
        #with open(f"{filename}.json") as json_file:
        #    data = json.load(json_file)
        os.system(f"rm {filename}")
        return  {
            'capitalFinal': 4500,
            'gain':2500,
            'loss':1500,
            'data':[
                {'Movimiento': '123a','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':500},
                {'Movimiento': '123b','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
                {'Movimiento': '123c','Volumen':3, 'OpenValue':1143.45, 'OpenIdx':25, 'CloseValue':1200.05,'CloseIdx':102, 'Balance':500},
                {'Movimiento': '123d','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
                {'Movimiento': '123e','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':-500},
                {'Movimiento': '123f','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':-500},
                {'Movimiento': '123g','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
                {'Movimiento': '123h','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':500},
                {'Movimiento': '123i','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
                {'Movimiento': '123j','Volumen':3, 'OpenValue':1183, 'OpenIdx':0, 'CloseValue':1159.45,'CloseIdx':1, 'Balance':-500},
                {'Movimiento': '123k','Volumen':3, 'OpenValue':1193.8,'OpenIdx':3, 'CloseValue':1195.82, 'CloseIdx':4, 'Balance':500},
            ]
        }