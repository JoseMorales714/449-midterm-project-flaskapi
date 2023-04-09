from flask import Flask, render_template, request, redirect, url_for, session, abort,jsonify
import pymysql
from flask_cors import CORS
import re
from datetime import timedelta

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# To connect MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password="pass123",
    db='',
    cursorclass=pymysql.cursors.DictCursor
)
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

