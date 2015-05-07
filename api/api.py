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

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.PointField(required = True)


class Happen(db.EmbeddedDocument):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    coordinates = db.PointField(required=False)
    type = db.StringField(max_length = 12, choices = ('mobility',
                                                      'security',
                                                      'service',
                                                      'other') , required = False)
    name = db.StringField(max_length = 115 , required = False)
    description = db.StringField(max_length = 255 , required = False)
    photo = db.ImageField(required = False)


class User(db.Document):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
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
        return url_for('post', kwargs = {"_id": self._id})

    def __unicode__(self):
        return self._id


class Via(db.Document):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    active = db.StringField(max_length = 5, choices = ('true',
                                                       'false'), default = 'true', required = False)
    name = db.StringField(max_length = 255, required = False)
    coordinatesPointA = db.PointField(required = True)
    coordinatesPointB = db.PointField(required = True)

    def get_absolute_url(self):
        return url_for('post', kwargs = {"_id": self._id})

    def __unicode__(self):
        return self._id


class Place(db.Document):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    active = db.StringField(max_length = 5, choices = ('true',
                                                       'false'), default = 'true', required = False)
    name = db.StringField(max_length = 255, required = False)
    coordinates = db.PointField(required = True)
    type = db.StringField(max_length = 25, choices = ('arts',
                                                      'ciclovia',
                                                      'culture',
                                                      'health',
                                                      'science',
                                                      'security',
                                                      'sport',
                                                      'technology',
                                                      'tourism',
                                                      'trade'), required = False)
    photo = db.ImageField(required = False)
    url = db.StringField(max_length = 300, default = 'true', required = False)

    def get_absolute_url(self):
        return url_for('post', kwargs = {"_id": self._id})

    def __unicode__(self):
        return self._id


class Benefit(db.Document):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    active = db.StringField(max_length = 5, choices = ('true',
                                                       'false'), default = 'false', required= True)
    startTime = db.DateTimeField(required = False)
    endTime = db.DateTimeField(required = False)

    name = db.StringField(max_length = 255, required = False)
    coordinates = db.PointField(required = True)
    category = db.StringField(max_length = 25, choices = ('event',
                                                          'service',
                                                          'safety'), required = False)

    type = db.StringField(max_length = 25, choices = ('arts',
                                                      'ciclovia',
                                                      'culture',
                                                      'health',
                                                      'science',
                                                      'security',
                                                      'sport',
                                                      'technology',
                                                      'tourism',
                                                      'trade'), required = False)

    cicloviaService = db.StringField(max_length = 25, choices = ('aerobics',
                                                      'baths',
                                                      'cycle ride',
                                                      'hydration point',
                                                      'loan bikes',
                                                      'pets point',
                                                      'RAFI',
                                                      'school bike'), required = False)

    description = db.StringField(max_length = 255, required = False)
    photo = db.ImageField(required = False)
    url = db.StringField(max_length = 300, default = 'true', required = False)

    def get_absolute_url(self):
        return url_for('post', kwargs = {"_id": self._id})

    def __unicode__(self):
        return self._id


class Notification(db.Document):

    createdAt = db.DateTimeField(default = datetime.datetime.now, required = True)
    active = db.StringField(max_length = 5, choices = ('true',
                                                       'false'), default = 'false', required= True)

    type = db.StringField(max_length = 25, choices = ('event',
                                                      'news',
                                                      'security',
                                                      'service'), required = False)

    priority = db.StringField(max_length = 25, choices = ('low',
                                                          'high',
                                                          'medium',
                                                          'none'), required = False)

    message = db.StringField(max_length = 255, required = True)
    photo = db.ImageField(required = False)
    url = db.StringField(max_length = 300, default = 'true', required = False)

    def get_absolute_url(self):
        return url_for('post', kwargs = {"_id": self._id})

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
            return json.loads(json.dumps({'user':User.objects(id = request.args.get('user_id'))})), status.HTTP_200_OK
        if request.args.get('age'):
            return json.loads(json.dumps({'user':User.objects(age = request.args.get('age'))})), status.HTTP_200_OK
        if request.args.get('gender'):
            return json.loads(json.dumps({'user':User.objects(gender = request.args.get('gender'))})), status.HTTP_200_OK
        if request.args.get('disability'):
            return json.loads(json.dumps({'user':User.objects(disability = request.args.get('disability'))})), status.HTTP_200_OK
        if request.args.get('healthRisk'):
            return json.loads(json.dumps({'user':User.objects(healthRisk = request.args.get('healthRisk'))})), status.HTTP_200_OK
        if request.args.get('activity'):
            return json.loads(json.dumps({'user':User.objects(activity = request.args.get('activity'))})), status.HTTP_200_OK
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
        return json.loads(json.dumps(user)), status.HTTP_201_CREATED
        #return "User created <br>"+json.loads(json.dumps(request.json))


@app.route('/users/locations' , methods = ['GET'])
def get_locations():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id = request.args.get('user_id')):
                return json.loads(json.dumps(user.locations)), status.HTTP_200_OK


@app.route('/users/locations', methods = ['POST'])
def new_location():
    if request.data:
        user = User.objects(id = request.args.get('user_id')).get()
        coord_lat= request.data.get("coord_lat")
        coord_lon= request.data.get("coord_len")
        my_point = geojson.Point((float(coord_lat), float(coord_lon)))
        l = Location.from_json(geojson.dumps(my_point, sort_keys = True))
        user.locations.append(l)
        user.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


@app.route('/users/happends' , methods = ['GET'])
def get_happends():
    if request.args:
        if request.args.get('user_id'):
            for user in User.objects(id = request.args.get('user_id')):
                #print "*"
                #print user.happends.photo
                return json.loads(json.dumps(user.happends)), status.HTTP_200_OK
    """else:
        for user in User.objects.all():
                return json.loads(json.dumps(user.happends)), status.HTTP_200_OK"""


@app.route('/users/happends', methods = ['POST'])
def new_happend():
    if request.data:
        user = User.objects(id = request.args.get('user_id')).get()

        coord_lat = request.data.get("coord_lat")
        coord_lon = request.data.get("coord_len")

        #temp_photo = open('/home/monica/Descargas/contest_winner.jpeg', 'rb')
        #path = params.get('file_path', None)
        #path = request.data.get("photo", None)
        #image = Image.open(path)
        #print image # **

        h = Happen(type = request.data.get("type"),
                 name = request.data.get("name"),
                 description = request.data.get("description"),
                 coordinates = [float(coord_lat), float(coord_lon)])
                 #,photo=image)

        h.photo.put(open(request.data.get('photo', None)))
        #print open(request.data.get('photo', None))
        #des.image.put(open(params.get('file_path', None)))

        user.happends.append(h)
        user.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


@app.route('/vias' , methods = ['GET'])
def get_vias():
    if request.args:
        if request.args.get('via_id'):
            return json.loads(json.dumps({'via':Via.objects(id = request.args.get('via_id'))})), status.HTTP_200_OK
        if request.args.get('name'):
            return json.loads(json.dumps({'via':Via.objects(name = request.args.get('name'))})), status.HTTP_200_OK
    else:
        return json.loads(json.dumps(Via.objects)), status.HTTP_200_OK


@app.route('/vias', methods = ['POST'])
def new_via():
    if request.data:
        coord_lat_pointA = float(request.data.get("coord_lat_pointA"))
        coord_len_pointA = float(request.data.get("coord_len_pointA"))
        coord_lat_pointB = float(request.data.get("coord_lat_pointB"))
        coord_len_pointB = float(request.data.get("coord_len_pointB"))

        via = Via(active = request.data.get("active"),
                 name = request.data.get("name"),
                 coordinatesPointA = [coord_lat_pointA, coord_len_pointA],
                 coordinatesPointB = [coord_lat_pointB, coord_len_pointB])

        via.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED
        #my_pointA = geojson.Point((coord_lat_pointA, coord_lon_pointA))
        #my_pointB = geojson.Point((coord_lat_pointB, coord_lon_pointB))
        #l = Location.from_json(geojson.dumps(my_point, sort_keys=True))


@app.route('/places' , methods = ['GET'])
def get_places():
    if request.args:
        if request.args.get('place_id'):
            return json.loads(json.dumps({'place':Place.objects(id = request.args.get('place_id'))})), status.HTTP_200_OK
        if request.args.get('name'):
            return json.loads(json.dumps({'place':Place.objects(name = request.args.get('name'))})), status.HTTP_200_OK
        if request.args.get('type'):
           return json.loads(json.dumps({'place':Place.objects(type = request.args.get('type'))})), status.HTTP_200_OK
    else:
        return json.loads(json.dumps(Place.objects)), status.HTTP_200_OK


@app.route('/places', methods = ['POST'])
def new_place():
    if request.data:
        coord_lat = request.data.get("coord_lat")
        coord_len = request.data.get("coord_len")

        place = Place(active = request.data.get("active"),
                 name = request.data.get("name"),
                 coordinates = [float(coord_lat), float(coord_len)],
                 type = request.data.get("type"),
                 url = request.data.get("url"))

        place.photo.put(open(request.data.get('photo', None)))
        place.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


@app.route('/benefits' , methods = ['GET'])
def get_benefits():
    if request.args:
        if request.args.get('benefit_id'):
            return json.loads(json.dumps({'benefit':Benefit.objects(id = request.args.get('benefit_id'))})), status.HTTP_200_OK
        if request.args.get('active'):
            return json.loads(json.dumps({'benefit':Benefit.objects(active = request.args.get('active'))})), status.HTTP_200_OK
        if request.args.get('startTime'):
            return json.loads(json.dumps({'benefit':Benefit.objects(startTime = request.args.get('startTime'))})), status.HTTP_200_OK
        if request.args.get('name'):
            return json.loads(json.dumps({'benefit':Benefit.objects(name = request.args.get('name'))})), status.HTTP_200_OK
        if request.args.get('category'):
            return json.loads(json.dumps({'benefit':Benefit.objects(category = request.args.get('category'))})), status.HTTP_200_OK
        if request.args.get('type'):
           return json.loads(json.dumps({'benefit':Benefit.objects(type = request.args.get('type'))})), status.HTTP_200_OK
        if request.args.get('cicloviaService'):
           return json.loads(json.dumps({'benefit':Benefit.objects(cicloviaService = request.args.get('cicloviaService'))})), status.HTTP_200_OK
    else:
        return json.loads(json.dumps(Benefit.objects)), status.HTTP_200_OK


@app.route('/benefits', methods = ['POST'])
def new_benefit():
    if request.data:
        coord_lat = request.data.get("coord_lat")
        coord_len = request.data.get("coord_len")

        benefit = Benefit(active = request.data.get("active"),
                          startTime = request.data.get("startTime"),
                          endTime = request.data.get("endTime"),
                          name = request.data.get("name"),
                          coordinates = [float(coord_lat), float(coord_len)],
                          category = request.data.get("category"),
                          type = request.data.get("type"),
                          cicloviaService = request.data.get("cicloviaService"),
                          description = request.data.get("description"),
                          url = request.data.get("url"))

        benefit.photo.put(open(request.data.get('photo', None)))
        benefit.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


@app.route('/notifications' , methods = ['GET'])
def get_notifications():
    if request.args:
        if request.args.get('notification_id'):
            return json.loads(json.dumps({'notification':Notification.objects(id = request.args.get('notification_id'))})), status.HTTP_200_OK
        if request.args.get('active'):
            return json.loads(json.dumps({'notification':Notification.objects(active = request.args.get('active'))})), status.HTTP_200_OK
        if request.args.get('type'):
            return json.loads(json.dumps({'notification':Notification.objects(type = request.args.get('type'))})), status.HTTP_200_OK
        if request.args.get('priority'):
            return json.loads(json.dumps({'notification':Notification.objects(priority = request.args.get('priority'))})), status.HTTP_200_OK
    else:
        return json.loads(json.dumps(Notification.objects)), status.HTTP_200_OK


@app.route('/notifications', methods = ['POST'])
def new_notification():
    if request.data:
        notification = Notification(active = request.data.get("active"),
                                    type = request.data.get("type"),
                                    priority = request.data.get("priority"),
                                    message = request.data.get("message"),
                                    url = request.data.get("url"))

        notification.photo.put(open(request.data.get('photo', None)))
        notification.save()
        return json.loads(json.dumps(request.data)), status.HTTP_201_CREATED


""" App main """
if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5000) )
	app.run( host = "0.0.0.0", port = port, debug = True )