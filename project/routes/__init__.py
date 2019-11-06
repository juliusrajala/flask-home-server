from flask import Blueprint
routes = Blueprint('routes', __name__)

from project.routes.test import *
from project.routes.files import *
