from flask import Flask,make_response, request, abort,jsonify
import pymysql
from flask_cors import CORS
import os
import jwt
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from pymysql.cursors import DictCursor


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'happykey'
# the below we ensure that we create a buffer for the file crednetials
# and ensuring the correct extension
app.config['SECRET_KEY']= 'key123'
app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.png']
app.config['UPLOAD_PATH'] = 'file'


# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="Cooldad@123",
    db='449_midterm',
    cursorclass=pymysql.cursors.DictCursor
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

    # Check if username has been used
    curr.execute("SELECT * FROM users WHERE username = % s", (username,))
    user = curr.fetchone()
    if user:
        return make_response("username has been used please try new one or login.", 401)

    # create new user
    curr.execute(
        "INSERT INTO users (username, password) VALUES (% s, % s)",
        (
         username,
         generate_password_hash(password),
        ),)
    conn.commit()
    return make_response("Successfully created!", 201)
 #Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
# check if username exists
    curr.execute("SELECT * FROM users WHERE username = % s", (username,))
    user = curr.fetchone()

    if not user:
        return make_response("USER DOESN't EXISTS!", 401)

    # check password
    if check_password_hash(user["password"], password):
        token = jwt.encode({"id": user["id"], "exp": datetime.utcnow() + timedelta(minutes=30)},
                           app.secret_key)
        return make_response(jsonify({"token": token}), 200)
    return make_response("could not verify user", 401,)


# upload
@app.route("/uploadfile", methods=['post'])
def uploadfile():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return make_response("file upload success")   # Making sure it was uploaded



if __name__ == "__main__":
    app.run(host="localhost", port=int("5300"))
