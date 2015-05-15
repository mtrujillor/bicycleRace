# -*- encoding: utf-8 -*-
from sqlalchemy.orm.strategy_options import loader_option

__author__ = 'xubuntu'

import geojson
import datetime
import os
import json
import urllib2
import random
import requests
import calendar
from random import randint
from random import randrange
from datetime import datetime
from datetime import timedelta


#list options test data
gender_list = ['female','male']
boolean_list = ['true', 'false']
disability_list = ['physical', 'hearing', 'visual','mental','other']
healthRisk_list = ['cardiovascular', 'breathing', 'infectious', 'bones joints muscles', 'other']
activity_list = ['bike riding', 'jogging', 'walking', 'skating', 'other']
happen_type_list = ['mobility', 'security', 'service','other']
place_type_list = ['arts', 'ciclovia', 'culture', 'health', 'science', 'security', 'sport', 'technology', 'tourism', 'trade']
benefits_category_list = ['event', 'service', 'safety']
benefits_type_list = ['arts', 'ciclovia', 'culture', 'health', 'science', 'security', 'sport', 'technology', 'tourism', 'trade']
benefits_cicloviaService_list = ['aerobics', 'baths', 'cycle ride', 'hydration point', 'loan bikes', 'pets point', 'RAFI', 'school bike']
notification_type_list = ['event', 'news', 'security', 'service']
notification_priority_list = ['low', 'high', 'medium', 'none']

#Paths
BASE_URL = 'http://0.0.0.0:5000'
USER_PATH = BASE_URL+'/users'
LOCATION_PATH = BASE_URL+'/users/locations'
HAPPEND_PATH = BASE_URL+'/users/happends'

#Point A
LAT_A = 4.697815
LONG_A = -74.033142
#Point B
LAT_B = 4.725423
LONG_B = -74.032455

user_list = []

def create_users():

    for x in range(0, 10):
        #Generate a user with random information
        user = get_new_user_json()

        #Call the API and store each user's information
        headers = ''
        r = requests.post(USER_PATH, headers=headers, data=user)
        saved_user = r.json()
        print saved_user
        user_list.append(saved_user)

def get_new_user_json():
    activity = 'bike riding' if random.random() < 0.4 else random.choice(activity_list)
    gender = random.choice(gender_list)
    age = randint(50, 80) if random.random() < 0.2 else randint(12, 49)
    disability = None if random.random() < 0.6 else random.choice(disability_list)
    health_risk = None if random.random() < 0.6 else random.choice(healthRisk_list)

    user = {"activity": activity,
            "gender": gender,
            "age": age,
            "disability": disability,
            "healthRisk": health_risk}
    return user

def users_travel(lat_a, long_a, lat_b, long_b):
    for user in user_list:

        lat_in = lat_a
        long_in = long_a
        lat_dest = lat_b
        long_dest = long_b

        #The user will randomly go from point a to b or viceversa
        if random.random() < 0.5:
            lat_in = lat_b
            long_in = long_b
            lat_dest = lat_a
            long_dest = long_a

        #The user will randomly make 4-8 posts along the way
        posts = randint(3, 7)

        #The user will enter the place between 7am and 1pm
        d1 = datetime.strptime('10/5/2015 7:00 AM', '%d/%m/%Y %I:%M %p')
        d2 = datetime.strptime('10/5/2015 1:00 PM', '%d/%m/%Y %I:%M %p')

        #The user will enter at any time of day
        entry_time = random_date(d1, d2)

        #The user will have different average times to travel depending on his travel method
        travel_time = randint(60*30, 60*55)
        travel_method = user['activity']
        if travel_method == 'bike riding':
            travel_time = randint(60*12, 60*25)
        if travel_method == 'jogging':
            travel_time = randint(60*18, 60*30)
        if travel_method == 'skating':
            travel_time = randint(60*14, 60*26)
        if travel_method == 'walking':
            travel_time = randint(60*25, 60*45)

        #Each post will need to go along the line the user is traversing
        for x in range(0, posts+1):
            progress = x/float(posts);
            lat_now = lat_in + (lat_dest - lat_in) * progress
            long_now = long_in + (long_dest - long_in) * progress

            now_time = entry_time + timedelta(seconds=travel_time * progress)
            epoch = datetime(1970,1,1)
            t = (now_time - epoch).total_seconds()
            print now_time
            print t
            #TODO
            #Offset the point by a little, they wont go in a straight line
            lat_now = lat_now + randint(-10,10)*0.0001
            #Call the API and store the location information
            location_request = {"coord_lat": lat_now, "coord_len": long_now, "timestamp": t}
            payload = {'user_id': user['_id']['$oid']}
            headers = ''
            r = requests.post(LOCATION_PATH, headers=headers, data=location_request, params=payload)
            print r.url

def create_happends():
    payload = {"user_id":user_list[0]['_id']['$oid']}
    h1 = {"coord_lat": 4.703589, "coord_len": -74.032745, "type": "security", "name": "Accidente en via", "description": "Carro chocó contra separador", "user_id":user_list[0]['_id']['$oid'], "timestamp":1431251155}
    requests.post(HAPPEND_PATH, data=h1, params=payload)
    h1 = {"coord_lat": 4.710261, "coord_len": -74.032938, "type": "service", "name": "Puesto de reparación", "description": "Puesto de reparación de bicicletas del distrito", "user_id":user_list[0]['_id']['$oid'], "timestamp":1431243729}
    requests.post(HAPPEND_PATH, data=h1, params=payload)
    h1 = {"coord_lat": 4.697494, "coord_len": -74.033024, "type": "service", "name": "Puesto de reparación", "description": "Puesto de reparación de bicicletas del distrito", "user_id":user_list[0]['_id']['$oid'], "timestamp":1431244931}
    requests.post(HAPPEND_PATH, data=h1, params=payload)
    h1 = {"coord_lat": 4.712849, "coord_len": -74.032766, "type": "mobility", "name": "Cierre temporal de calle", "description": "Cierre temporal de cruce por accidente", "user_id":user_list[0]['_id']['$oid'], "timestamp":1431263072}
    requests.post(HAPPEND_PATH, data=h1, params=payload)

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

create_users()
create_happends()
users_travel(LAT_A, LONG_A, LAT_B, LONG_B)
#print json.load(urllib2.urlopen("http://0.0.0.0:5000/users"))

