# -*- coding: utf-8 -*-

from locust import HttpLocust, TaskSet, task
import random
from random import randint
from faker import Factory


fake = Factory.create('en_US')


#test data local
user_id_list = ['55247d1dbd3cc61754617ede', '55247d1fbd3cc61754617ee4']
photo = '/home/monica/Descargas/contest_winner.jpeg'

via_id = '55247d1ebd3cc61754617edf'
via_name = 'Colby Mission'

place_id = '55247d25bd3cc61754617eed'
place_name = 'Hane'

benefit_id = '55247d21bd3cc61754617ee9'
benefits_name = 'Qui rerum maiores dolor.'

notification_id = '55247d1ebd3cc61754617ee3'


"""
#test data cloud
user_id_list = ['552576a566ce06000a946cc6','552576a966ce06000a946cc7']
photo = '/home/monica/Descargas/contest_winner.jpeg'

via_id = '552576b766ce06000a946cc8'
via_name = 'Dorothea Locks'

#pendiente
place_id = '55247d25bd3cc61754617eed'
place_name = 'Hane'

benefit_id = '55247d21bd3cc61754617ee9'
benefits_name = 'Qui rerum maiores dolor.'

notification_id = '55247d1ebd3cc61754617ee3'
"""

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

benefits_cicloviaService_list = ['aerobics', 'baths', 'cycle ride', 'hydration point', 'loan bikes', 'pets point', 'RAFI','school bike']

notification_type_list = ['event','news','security','service']

notification_priority_list = ['low', 'high', 'medium', 'none']


class UserBehavior(TaskSet):

    @task(1)
    def api_root(self):
        response = self.client.get("/")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_users(self):
        response = self.client.get("/users")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_user_by_user(self):
        response = self.client.get("/users?user_id="+random.choice(user_id_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_user_by_age(self):
        age = randint(5,80)
        response = self.client.get("/users?age="+str(age))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_user_by_gender(self):
        response = self.client.get("/users?gender="+random.choice(gender_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(2)
    def get_user_by_disability(self):
        response = self.client.get("/users?disability="+random.choice(disability_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(2)
    def get_user_by_healthRisk(self):
        response = self.client.get("/users?healthRisk="+random.choice(healthRisk_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(4)
    def get_user_by_activity(self):
        response = self.client.get("/users?activity="+random.choice(activity_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(7)
    def new_user(self):
        #response = self.client.post("/users", {"activity": "bike riding",
        age = randint(5,80)
        self.client.post("/users", {"activity": random.choice(activity_list),
                                    "gender":random.choice(gender_list),
                                    "age": age,
                                    "disability": random.choice(disability_list),
                                    "healthRisk": random.choice(healthRisk_list)})

    @task(2)
    def get_locations(self):
        response = self.client.get("/users/locations?user_id="+random.choice(user_id_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(9)
    def new_location(self):
        lat = randint(-90,90)
        len = randint(-90,90)
        response = self.client.post("/users/locations?user_id=" + random.choice(user_id_list), {"coord_lat":lat,
                                                                            "coord_len":len})
        print "Response status code:", response.status_code
        print "Response content:", response.content

    @task(2)
    def get_happends(self):
        response = self.client.get("/users/happends?user_id=" + random.choice(user_id_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(5)
    def new_happend(self):
        lat = randint(-90,90)
        len = randint(-90,90)
        response = self.client.post("/users/happends?user_id=" + random.choice(user_id_list), { "type" : random.choice(happen_type_list),
                                                                         "name" : fake.sentence(nb_words=4),
                                                                         "description" : fake.sentence(nb_words=10),
                                                                         "coord_lat" : lat,
                                                                         "coord_len" : len,
                                                                         "photo" : photo})
        print "Response status code:", response.status_code
        print "Response content:", response.content

    @task(2)
    def get_vias(self):
        response = self.client.get("/vias")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_vias_by_id(self):
        response = self.client.get("/vias?via_id="+via_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_vias_by_name(self):
        response = self.client.get("/vias?name="+via_name)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def new_via(self):
        number = randint(0,200)
        lat_A = randint(-90,90)
        len_A = randint(-90,90)
        lat_B = randint(-90,90)
        len_B = randint(-90,90)
        response = self.client.post("/vias", {"active":"true",
                                              "name": fake.street_name(),
                                              "coord_lat_pointA":lat_A,
                                              "coord_len_pointA":len_A,
                                              "coord_lat_pointB":lat_B,
                                              "coord_len_pointB":len_B})
        print "Response status code:", response.status_code

    @task(3)
    def get_places(self):
        response = self.client.get("/places")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_places_by_id(self):
        response = self.client.get("/places?place_id="+place_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_places_by_name(self):
        response = self.client.get("/places?name="+place_name)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_places_by_type(self):
        response = self.client.get("/places?type="+random.choice(place_type_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def new_place(self):
        lat = randint(-90,90)
        len = randint(-90,90)
        response = self.client.post("/places", {"type": random.choice(place_type_list),
                                                "name": fake.last_name(),
                                                "coord_lat":lat,
                                                "coord_len":len,
                                                "url": fake.url(),
                                                "photo":photo})
        print "Response status code:", response.status_code
        print "Response content:", response.content

    @task(3)
    def get_benefits(self):
        response = self.client.get("/benefits")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_benefits_by_id(self):
        response = self.client.get("/benefits?benefit_id="+benefit_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_benefits_by_active(self):
        response = self.client.get("/benefits?active="+random.choice(boolean_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    """Make this
    @task(2)
    def get_benefits_by_startime(self):
        response = self.client.get()
        print "Response status code:", response.status_code
        #print "Response content:", response.content"""

    @task(4)
    def get_benefits_by_name(self):
        response = self.client.get("/benefits?name="+benefits_name)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(4)
    def get_benefits_by_category(self):
        response = self.client.get("/benefits?category="+random.choice(benefits_category_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(4)
    def get_benefits_by_type(self):
        response = self.client.get("/benefits?type="+random.choice(benefits_type_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(4)
    def get_benefits_by_cicloviaService(self):
        response = self.client.get("/benefits?cicloviaService="+random.choice(benefits_cicloviaService_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def new_benefit(self):
        lat = randint(-90,90)
        len = randint(-90,90)
        response = self.client.post("/benefits", {"active":random.choice(boolean_list),
                                                  "name": fake.sentence(nb_words=3),
                                                  "coord_lat":lat,
                                                  "coord_len":len,
                                                  "category": random.choice(benefits_category_list),
                                                  "type": random.choice(benefits_type_list),
                                                  "cicloviaService": random.choice(benefits_cicloviaService_list),
                                                  "description": fake.sentence(nb_words=10),
                                                  "url": fake.url(),
                                                  "photo": photo})
        print "Response status code:", response.status_code

    @task(2)
    def get_notifications(self):
        response = self.client.get("/notifications")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_notifications_by_id(self):
        response = self.client.get("/notifications?notification_id="+notification_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_notifications_active(self):
        response = self.client.get("/notifications?active="+random.choice(boolean_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_notifications_type(self):
        response = self.client.get("/notifications?type="+random.choice(notification_type_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(3)
    def get_notifications_priority(self):
        response = self.client.get("/notifications?priority="+random.choice(notification_priority_list))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def new_notifications(self):
        response = self.client.post("/notifications", {"active": random.choice(boolean_list),
                                                       "type": random.choice(notification_type_list),
                                                       "priority": random.choice(notification_priority_list),
                                                       "message": fake.sentence(nb_words=20),
                                                       "url": fake.url(),
                                                       "photo": photo})
        print "Response status code:", response.status_code
        print "Response content:", response.content


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=4000
    max_wait=7000