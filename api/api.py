"""import settings"""
import os
import datetime     #models
from flask import Flask, url_for, request, Response, json, jsonify
from flask.ext.script import Manager, Server
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from flask import abort
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)

""" Database connection settings"""
dbName = 'my_api_va'
dbPass = 'KeepThisS3cr3t'
app.config["MONGODB_SETTINGS"] = {'DB':dbName }
app.config["SECRET_KEY"] = dbPass
db = MongoEngine(app)


""" Mongodb collections"""
class Round(db.EmbeddedDocument):
    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.StringField(max_length = 25, required = True) #example 41 24.2028, 2 10.4418


class User(db.Document):

    genderCode = {'F': 'female',
                  'M': 'male'}

    disabilityCode = {'PHY': 'physical',
                      'HEA': 'hearing',
                      'VIS': 'visual',
                      'MEN':'mental',
                      'OTH':'other'}

    healthRiskCode = {'CARD': 'cardiovascular',
                      'BREA': 'breathing',
                      'INFE': 'infectious',
                      'BJM':'bones joints muscles',
                      'OTH':'other'}

    activityCode = {'BIK': 'bike riding',
                    'JOG': 'jogging',
                    'WALK': 'walking',
                    'SKATE':'skating',
                    'OTH':'other'}

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    age = db.IntField(required = False)
    gender = db.StringField(max_length = 6, choices = genderCode.keys() , required = False)
    disability = db.StringField(max_length = 12, choices = disabilityCode.keys() , required = False)
    healthRisk = db.StringField(max_length = 22, choices = healthRiskCode.keys() , required = False)
    activity = db.StringField(max_length = 12, choices = activityCode.keys() , required = False)
    rounds = db.ListField(db.EmbeddedDocumentField(Round))


    def get_absolute_url(self):
        return url_for('post', kwargs={"_id": self._id})

    def __unicode__(self):
        return self._id


""" App routes """
@app.route('/')
def api_root():
    return 'Welcome API Bicycle Race :)'

@app.route('/users/' , methods = ['GET'])
def get_users():
    if request.args:
        if request.args.get('user_id'):
            return jsonify({'user':User.objects.get_or_404(id=request.args.get('user_id'))})
        if request.args.get('age'):
            return jsonify({'user':User.objects.get_or_404(age=request.args.get('age'))})
        if request.args.get('gender'):
            return jsonify({'user':User.objects.get_or_404(gender=request.args.get('gender'))})
        if request.args.get('disability'):
            return jsonify({'user':User.objects.get_or_404(disability=request.args.get('disability'))})
        if request.args.get('healthRisk'):
            return jsonify({'user':User.objects.get_or_404(healthRisk=request.args.get('healthRisk'))})
        if request.args.get('activity'):
            return jsonify({'user':User.objects.get_or_404(activity=request.args.get('activity'))})
    else:
        return jsonify({'user':User.objects.all()})     #or return User.objects.all().to_json()

@app.route('/users/', methods=['POST'])
def new_user():
    if request.json:
        user = User.from_json(json.dumps(request.json))
        user.save()
        return jsonify({})

@app.route('/users/rounds/' , methods = ['GET'])
def get_rounds():
    if request.args:
        if request.args.get('coordinates'):
            return jsonify({'round':User.objects.get_or_404(coordinates=request.args.get('coordinates'))})
    else:
        return jsonify({'rounds':Round.objects.all()})     #or return User.objects.all().to_json()

@app.route('/users/rounds/', methods=['POST'])
def new_round():
    if request.json:
        print "band1"
        user = User.objects(id=request.args.get('user_id')).get()
        print "band2"
        r = Round.from_json(json.dumps(request.json))
        print "band3"
        user.rounds.append(r)
        print "band4"
        user.save()
        print "band4"
        return jsonify({})


""" App main """
if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5000) )
	app.run( host = "0.0.0.0", port = port, debug = True )
