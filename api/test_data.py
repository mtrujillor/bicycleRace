from sqlalchemy.orm.strategy_options import loader_option

__author__ = 'xubuntu'

import geojson
import datetime
import os
import json
import urllib2
import random
import requests
from random import randint


user_list = None

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

def user_travel(lat_in, long_in, lat_dest, long_dest):
    for user in user_list:
        #The user will randomly make 4-8 posts along the way
        posts = randint(1, 1)

        #Each post will need to go along the line the user is traversing
        for x in range(0, posts):
            progress = x/posts;
            lat_now = lat_in + (lat_dest - lat_in) * progress
            long_now = long_in + (long_dest - long_in) * progress

            #TODO
            #Offset the point by a little, they wont go in a straight line

            #Call the API and store the location information
            location_request = {"coord_lat": lat_now, "coord_len": long_now}
            payload = {'user_id': user['_id']['$oid']}
            headers = ''
            r = requests.post(LOCATION_PATH, headers=headers, data=location_request, params=payload)
            print r.url

create_users()
user_travel(19.88, 9.88, 20.88, 10.88)
#print json.load(urllib2.urlopen("http://0.0.0.0:5000/users"))

