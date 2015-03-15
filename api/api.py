"""import settings"""
import os
import datetime     #models
from flask import Flask, url_for, request, Response, json, jsonify
from flask.ext.script import Manager, Server
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from bson import json_util


app = Flask(__name__)

""" Database connection settings"""
dbName = 'my_api_va'
dbPass = 'KeepThisS3cr3t'
app.config["MONGODB_SETTINGS"] = {'DB':dbName }
app.config["SECRET_KEY"] = dbPass
db = MongoEngine(app)


""" Mongodb collections"""
class User(db.Document):

    genderCode = {'F': 'female',
                  'M': 'male'}

    activityCode = {'BIK': 'bike riding',
                    'JOG': 'jogging',
                    'WALK': 'walking',
                    'SKATE':'skating',
                    'OTH':'other'}

    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    age = db.IntField(required = False)
    gender = db.StringField(max_length = 6, choices = genderCode.keys() , required = False)
    activity = db.StringField(max_length = 20, choices = activityCode.keys() , required = False)

    def get_absolute_url(self):
        return url_for('post', kwargs={"_id": self._id})

    def __unicode__(self):
        return self._id

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', '_id'],
        'ordering': ['-created_at']
    }


""" User routes """
@app.route('/')
def api_root():
    return 'Welcome API Bicycle Race :)'

@app.route('/users' , methods = ['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        return User.objects.all().to_json()
    elif request.method == 'POST':
        mydata=request.json
        if request.json:
            user = User.from_json(json.dumps(request.json))
            user.save()
            return "Thanks. Your age is %s" % mydata.get("age")
        else:
            return "no json received"

#prueba para guardar usuarios
@app.route('/users_save' , methods = ['POST'])
def api_users_save():
	#message=request.form['message']
	#if not message:
	#	message="ejercitarse"
	user = User()
	user.age = 55
	user.activity='JOG'
	user.save()
	return "ready :D "

""" App main """
if __name__ == '__main__':
	port = int( os.environ.get("PORT", 5000) )
	app.run( host = "0.0.0.0", port = port, debug = True )
