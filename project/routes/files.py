from flask import escape, request
from project.routes import routes

@routes.route('/v1/file/upload')
def upload_file():
    return 'Uploading file'

@routes.route('/v1/file/')
def get_files():
    return 'All files'
