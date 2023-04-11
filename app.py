from flask import Flask, render_template, request, redirect, url_for, session, abort,jsonify
import pymysql
from flask_cors import CORS
import re
from datetime import timedelta

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['UPLOAD_PATH'] = 'uploads'



# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="pass123",
    db='',
    cursorclass=pymysql.cursors.DictCursor
)

# def upload_files():
#     uploaded_file = request.files['file']
#     filename = secure_filename(uploaded_file.filename)
#     if filename != '':
#         file_ext = os.path.splitext(filename)[1]
#         if file_ext not in app.config['UPLOAD_EXTENSIONS']:
#             abort(400)
#         uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
#         return redirect(url_for('index'))



# Error handling
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)),401

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)),404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)),500

@app.errorhandler(415)
def unsupported_media_type(e):
    return jsonify(error=str(e)),415

