import os
from flask import current_app as app, Blueprint, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename
import uuid

blueprint = Blueprint('public', __name__)

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@blueprint.route('/')
def home():
    if request.method == 'GET':
        return render_template('home.html')


@blueprint.route('/public/about')
def about():
    return render_template('about.html')

@blueprint.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = str(uuid.uuid1())
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(os.path.join(app.config['APP_DIR'],app.config['UPLOAD_FOLDER']), filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        # return redirect(url_for('public.uploaded_file', filename=filename))
        return redirect(url_for('public.graph', filename=filename))


@blueprint.route('/graph/<filename>', methods=['GET'])
def graph(filename):
    return render_template('graph.html', filename=filename)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    # render_template('graph.html',filename)
    return send_from_directory(os.path.join(app.config['APP_DIR'],app.config['UPLOAD_FOLDER']), filename)