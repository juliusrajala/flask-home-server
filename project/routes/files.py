from flask import escape, request, flash, redirect
from project.routes import routes
from project.utils.logging import print_out

@routes.route('/v1/file/upload', methods=['POST', 'GET'])
def upload_file():
    print_out(f'Attempting to upload {request}')
    if request.method == 'GET':
        return 'Upload files as data'
    if 'file' not in request.files:
        print_out(f'No file in request {request.files}')
        flash(f'No file in request {request.files}')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print_out('No file selected for uploading')
        return redirect(request.url)
    print_out(f'File is uploaded {file}')
    return 'Uploading file'

@routes.route('/v1/file/meta', methods=['POST'])
def file_data():
    print_out(request.json)
    return 'Thanks for the meta'

@routes.route('/v1/files/')
def get_files():
    return 'All files'
