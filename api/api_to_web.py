import os
import datetime     #models
from flask import Flask, url_for, request, Response, json, jsonify
from flask import render_template
from flask.ext.api import FlaskAPI, status, exceptions
import requests

BASE_URL = 'http://0.0.0.0:5000'
USER_PATH = BASE_URL+'/users'
LOCATION_PATH = BASE_URL+'/users/locations'

app = Flask(__name__)

@app.route('/users')
def api_root():
    resp = requests.get(USER_PATH)
    return (resp.text, resp.status_code, resp.headers.items())

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5001) )
	app.run( host = "0.0.0.0", port = port, debug = True )