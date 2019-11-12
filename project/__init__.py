import logging
from flask import Flask
from project.routes import routes

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(routes)
