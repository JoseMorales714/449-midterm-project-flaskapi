from flask import Flask, render_template,make_response, request, redirect, url_for, session, abort,jsonify
import pymysql
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'happykey'
# the below we ensure that we create a buffer for the file crednetials
# and ensuring the correct extension
app.config['SECRET_KEY']= 'key123'
app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.png']
app.config['UPLOAD_PATH'] = 'uploads'


# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="passcode",
    db='449_midterm',
)

curr = conn.cursor()
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

@app.route("/")

# public for anyone to see
@app.route("/public")
def public():
    return make_response("For Everyone!")
# sign up to create account
@app.route("/signup", methods =['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    # check if anything is missing
    if not username or not password:
        return make_response("Missing Username or Password.", 400,)
    # create new user
    curr.execute(
        "INSERT INTO users (username, password) VALUES (% s, % s)",
        (
         username,
         generate_password_hash(password),
        ),
)
    conn.commit()
    return make_response("Successfully created!", 201)

@app.route("/uploadfile", methods=['post'])
def uploadfile():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return make_response("file upload success")



if __name__ == "__main__":
    app.run(host="localhost", port=int("5300"))
