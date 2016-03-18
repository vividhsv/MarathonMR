import os
from flask import current_app as app, Blueprint, render_template, request, url_for, redirect, send_from_directory, flash
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


@blueprint.route('/about')
def about():
    return render_template('about.html')


@blueprint.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        flash("Please select a file to upload.", 'error')
        return redirect(url_for('public.home'))
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid1())
        file.save(os.path.join(os.path.join(app.config['APP_DIR'],app.config['UPLOAD_FOLDER']), filename))
        return redirect(url_for('public.graph', filename=filename))


@blueprint.route('/graph/<filename>', methods=['GET'])
def graph(filename):
    return render_template('graph.html', filename=filename)


@blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['APP_DIR'],app.config['UPLOAD_FOLDER']), filename)