from flask import escape, request
from project.routes import routes

@routes.route('/test/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@routes.route('/')
def root():
    route = "root route"
    return f'This is the {route}'

@routes.route('/haloo')
def haloo():
    return 'Huhuu!'