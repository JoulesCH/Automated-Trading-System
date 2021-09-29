from flask_restful import reqparse

post_args = reqparse.RequestParser()
arguments = [
    {'nombre':'subcategoria', 'type': str, 'help':'subcategoria es requerida y de tipo str','required':True},
]

for argument in arguments:
    post_args.add_argument(argument['nombre'], 
                                 type = argument['type'], 
                                 help = argument['help'],
                                 required=argument['required']
                    )