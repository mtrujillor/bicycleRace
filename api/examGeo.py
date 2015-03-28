import geojson
from flask.ext.mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from flask.ext.api import FlaskAPI, status, exceptions


app = FlaskAPI(__name__)


""" Database connection settings"""
dbName = 'example_geos'
dbPass = 'KeepThisS3cr3t'
app.config["MONGODB_SETTINGS"] = {'DB':dbName }
app.config["SECRET_KEY"] = dbPass
db = MongoEngine(app)

class Location(db.Document):
    coord = db.PointField(required=True)  # GeoJSON

my_point = geojson.Point((45.24, -1.532))
dump = geojson.dumps(my_point, sort_keys=True)
print "my_point"
print my_point
print "dump"
print dump
print "geojson.loads(dump)"
print geojson.loads(dump)

print "d"
a = Location(geojson.Point((55.24, -1.532)))
a.save()

"""print "a"
a = Location(my_point)
a.save()"""

"""print "b"
b = Location(dump)
b.save()

print "c"
c = Location(geojson.loads(dump))
c.save()"""

print "do !!!"



if __name__ == "__main__":
    app.run(debug=True)
