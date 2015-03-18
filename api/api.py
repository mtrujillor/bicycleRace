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
class Location(db.EmbeddedDocument):
    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.StringField(max_length = 25, required = True) #example 41 24.2028, 2 10.4418


class Happen(db.EmbeddedDocument):

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.StringField(max_length = 25, required = False)
    type = db.StringField(max_length = 12, choices = ('mobility',
                                                      'security',
                                                      'service',
                                                      'other') , required = False)
    name = db.StringField(max_length = 115 , required = False)
    description = db.StringField(max_length = 255 , required = False)


class User(db.Document):

    genderCode = {'F': 'female',
                  'M': 'male'}

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    age = db.IntField(required = False)
    gender = db.StringField(max_length = 6, choices = genderCode.keys() , required = False)
    disability = db.StringField(max_length = 12, choices = ('physical',
                                                            'hearing',
                                                            'visual',
                                                            'mental',
                                                            'other') , required = False)
    healthRisk = db.StringField(max_length = 22, choices = ('cardiovascular',
                                                            'breathing',
                                                            'infectious',
                                                            'bones joints muscles',
                                                            'other') , required = False)
    activity = db.StringField(max_length = 12, choices = ('bike riding',
                                                          'jogging',
                                                          'walking',
                                                          'skating',
                                                          'other') , required = False)
    locations = db.ListField(db.EmbeddedDocumentField(Location))
    happends = db.ListField(db.EmbeddedDocumentField(Happen))

    def get_absolute_url(self):
        return url_for('post', kwargs={"_id": self._id})

    def __unicode__(self):
        return self._id


""" App routes """
@app.route('/')
def api_root():
    return 'Welcome API Bicycle Race :)'


@app.route('/users' , methods = ['GET'])
def get_users():
    if request.args:
        if request.args.get('user_id'):
            return jsonify({'user':User.objects(id=request.args.get('user_id'))})
        if request.args.get('age'):
            return jsonify({'user':User.objects(age=request.args.get('age'))})
        if request.args.get('gender'):
            return jsonify({'user':User.objects(gender=request.args.get('gender'))})
        if request.args.get('disability'):
            return jsonify({'user':User.objects(disability=request.args.get('disability'))})
        if request.args.get('healthRisk'):
            return jsonify({'user':User.objects(healthRisk=request.args.get('healthRisk'))})
        if request.args.get('activity'):
            return jsonify({'user':User.objects(activity=request.args.get('activity'))})
    """else:
        return jsonify({'user':User.objects.all()})     #or return User.objects.all().to_json()"""

@app.route('/users', methods=['POST'])
def new_user():
    if request.json:
        user = User.from_json(json.dumps(request.json))
        user.save()
        return "User created <br>"+json.dumps(request.json)


@app.route('/users/locations' , methods = ['GET'])
def get_locations():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id=request.args.get('user_id')):
                return jsonify({'locations':user.locations})
            #return jsonify({'location':User.objects(id=request.args.get('user_id'))})
        #elif request.args.get('coordinates'):
         #   return jsonify({'location':User.objects(coordinates=request.args.get('coordinates'))})
    """else:
        for user in User.objects(locations!=null):
            return jsonify({'locations':user.locations})"""

@app.route('/users/locations', methods=['POST'])
def new_location():
    if request.json:
        user = User.objects(id=request.args.get('user_id')).get()
        r = Location.from_json(json.dumps(request.json))
        user.locations.append(r)
        user.save()
        return "Location created <br>"+json.dumps(request.json)


@app.route('/users/happends' , methods = ['GET'])
def get_happends():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id=request.args.get('user_id')):
                return jsonify({'happends':user.happends})
        #if request.args.get('type'):
        #    return jsonify({'user':User.happends(type=request.args.get('type'))})
    else:
        for user in User.objects.all():
                return jsonify({'happends':user.happends})

@app.route('/users/happends', methods=['POST'])
def new_happend():
    if request.json:
        user = User.objects(id=request.args.get('user_id')).get()
        h = Happen.from_json(json.dumps(request.json))
        user.happends.append(h)
        user.save()
        return "Happend created <br>"+json.dumps(request.json)


""" App main """
if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5000) )
	app.run( host = "0.0.0.0", port = port, debug = True )
