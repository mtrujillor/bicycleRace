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
from flask.ext.api import FlaskAPI, status, exceptions
from flask.ext.api.renderers import JSONRenderer
import tempfile
import geojson
from PIL import Image



app = FlaskAPI(__name__)

app.config['DEFAULT_RENDERERS'] = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

""" Database connection settings"""
dbName = 'my_api_va'
dbPass = 'KeepThisS3cr3t'
app.config["MONGODB_SETTINGS"] = {'DB':dbName }
app.config["SECRET_KEY"] = dbPass
db = MongoEngine(app)


""" Mongodb collections"""
class Location(db.EmbeddedDocument):
    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.PointField(required=True)


class Happen(db.EmbeddedDocument):

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.PointField(required=False)
    type = db.StringField(max_length = 12, choices = ('mobility',
                                                      'security',
                                                      'service',
                                                      'other') , required = False)
    name = db.StringField(max_length = 115 , required = False)
    description = db.StringField(max_length = 255 , required = False)
    photo = db.ImageField()


class User(db.Document):

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    age = db.IntField(required = False)
    gender = db.StringField(max_length = 6, choices = ('female',
                                                        'male'), required = False)
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
            return json.loads(json.dumps({'user':User.objects(id=request.args.get('user_id'))})), status.HTTP_200_OK
        if request.args.get('age'):
            return json.loads(json.dumps({'user':User.objects(age=request.args.get('age'))})), status.HTTP_200_OK
        if request.args.get('gender'):
            return json.loads(json.dumps({'user':User.objects(gender=request.args.get('gender'))})), status.HTTP_200_OK
        if request.args.get('disability'):
            return json.loads(json.dumps({'user':User.objects(disability=request.args.get('disability'))})), status.HTTP_200_OK
        if request.args.get('healthRisk'):
            return json.loads(json.dumps({'user':User.objects(healthRisk=request.args.get('healthRisk'))})), status.HTTP_200_OK
        if request.args.get('activity'):
            return json.loads(json.dumps({'user':User.objects(activity=request.args.get('activity'))})), status.HTTP_200_OK
    else:
        return json.loads(json.dumps(User.objects)), status.HTTP_200_OK
        #return return jsonify(User.objects) #works but no pretty
        #return Response(json.dumps(User.objects()),  mimetype='application/json') #works pretty with postman
        #return json.dumps(User.objects,indent=4, separators=(',', ': '), ensure_ascii=False) #works but no pretty

@app.route('/users', methods=['POST'])
def new_user():
    if request.data:
        user = User.from_json(json.dumps(request.data))
        user.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED
        #return "User created <br>"+json.loads(json.dumps(request.json))


@app.route('/users/locations' , methods = ['GET'])
def get_locations():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id=request.args.get('user_id')):
                return json.loads(json.dumps(user.locations)), status.HTTP_200_OK


@app.route('/users/locations', methods=['POST'])
def new_location():
    if request.data:
        user = User.objects(id=request.args.get('user_id')).get()
        coord_lat= request.data.get("coord_lat")
        coord_lon= request.data.get("coord_len")
        my_point = geojson.Point((coord_lat, coord_lon))
        l = Location.from_json(geojson.dumps(my_point, sort_keys=True))
        user.locations.append(l)
        user.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


@app.route('/users/happends' , methods = ['GET'])
def get_happends():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id=request.args.get('user_id')):
                #print "*"
                #print user.happends.photo
                return json.loads(json.dumps(user.happends)), status.HTTP_200_OK
    else:
        for user in User.objects.all():
                return json.loads(json.dumps(user.happends)), status.HTTP_200_OK

@app.route('/users/happends', methods=['POST'])
def new_happend():
    if request.data:
        user = User.objects(id=request.args.get('user_id')).get()

        coord_lat= request.data.get("coord_lat")
        coord_lon= request.data.get("coord_len")

        #temp_photo = open('/home/monica/Descargas/contest_winner.jpeg', 'rb')
        #path = params.get('file_path', None)
        #path = request.data.get("photo", None)
        #image = Image.open(path)
        #print image # **

        h=Happen(type=request.data.get("type"),
                 name=request.data.get("name"),
                 description=request.data.get("description"),
                 coordinates=[coord_lat, coord_lon])
                 #,photo=image)

        h.photo.put(open(request.data.get('photo', None)))
        print open(request.data.get('photo', None))
        #des.image.put(open(params.get('file_path', None)))

        user.happends.append(h)
        user.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


""" App main """
if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5000) )
	app.run( host = "0.0.0.0", port = port, debug = True )