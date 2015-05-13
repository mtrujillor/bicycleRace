import os
import datetime     #models
from twisted.web.xmlrpc import payloadTemplate
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
    payload = {}
    dictionary = {}
    if request.args.get('user_id'):
        dictionary['user_id'] = request.args.get('user_id')
    if request.args.get('age'):
        dictionary['age'] = request.args.get('age')
    if request.args.get('gender'):
        dictionary['gender'] = request.args.get('gender')
    if request.args.get('disability'):
        dictionary['disability'] = request.args.get('disability')
    if request.args.get('healthRisk'):
        dictionary['healthRisk'] = request.args.get('healthRisk')
    if request.args.get('activity'):
        dictionary['activity'] = request.args.get('activity')
    if request.args.get('date_start'):
        time = datetime.datetime.strptime(request.args.get('date_start'), '%d/%m/%Y %H:%M')
        dictionary['date_start'] = (time - datetime.datetime(1970, 1, 1)).total_seconds()
    if request.args.get('date_end'):
        time = datetime.datetime.strptime(request.args.get('date_end'), '%d/%m/%Y %H:%M')
        dictionary['date_end'] = (time - datetime.datetime(1970, 1, 1)).total_seconds()
    if request.args.get('age_start'):
        dictionary['age_start'] = request.args.get('age_start')
    if request.args.get('age_end'):
        dictionary['age_end'] = request.args.get('age_end')
    resp = requests.get(USER_PATH, params=dictionary)
    text = resp.text
    return Response(text, mimetype='application/json')

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5001) )
	app.run( host = "0.0.0.0", port = port, debug = True )