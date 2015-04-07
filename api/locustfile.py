from locust import HttpLocust, TaskSet, task
from random import randint


#test data
user_id = "55230e89bd3cc668fe73131f"
photo = "/home/monica/Descargas/contest_winner.jpeg"
age = 28
gender = "female"
disability = "visual"
healthRisk = "cardiovascular"
activity = "bike riding"
via_id = "55174336bd3cc63d999fe0f7"
via_name = "AV 26"
place_id = "551c6756bd3cc614b1586bf4"
place_name = "Cerro monserrate"
place_type = "tourism"
benefit_id = "551c7b77bd3cc629c7de8f02"
benefits_active = "true"
benefits_name = "aerobicos Salitre"
benefits_category = "service"
benefits_type = "sport"
benefits_cicloviaService = "aerobics"
notification_id = "551e021ebd3cc62ce41d6735"
notification_active = "true"
notification_type = "news"
notification_priority = "medium"

class UserBehavior(TaskSet):

    @task()
    def api_root(self):
        response = self.client.get("/")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_users(self):
        response = self.client.get("/users")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_user_by_user(self):
        response = self.client.get("/users?user_id="+user_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_user_by_age(self):
        response = self.client.get("/users?age="+str(age))
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_user_by_age(self):
        response = self.client.get("/users?age="+age)
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(1)
    def get_user_by_gender(self):
        response = self.client.get("/users?gender="+gender)
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(1)
    def get_user_by_disability(self):
        response = self.client.get("/users?disability="+disability)
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(1)
    def get_user_by_healthRisk(self):
        response = self.client.get("/users?healthRisk="+healthRisk)
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(1)
    def get_user_by_activity(self):
        response = self.client.get("/users?activity="+activity)
        print "Response status code:", response.status_code
        #print "Response content:", response.conten

    @task(3)
    def new_user(self):
        #response = self.client.post("/users", {"activity": "bike riding",
        self.client.post("/users", {"activity": "bike riding",
                                    "gender":"male",
                                    "age": 52,
                                    "healthRisk":"cardiovascular"})

    @task(2)
    def get_locations(self):
        response = self.client.get("/users/locations?user_id="+user_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(8)
    def new_location(self):
        lat = randint(-90,90)
        len = randint(-180,180)
        response = self.client.post("/users/locations?user_id=" + user_id, {"coord_lat":lat,
                                                                            "coord_len":len})
        print "Response status code:", response.status_code

    @task(1)
    def get_happends(self):
        response = self.client.get("/users/happends?user_id=" + user_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(6)
    def new_happend(self):
        lat = randint(-90,90)
        len = randint(-180,180)
        response = self.client.post("/users/happends?user_id=" + user_id, { "type" : "mobility",
                                                                         "name" : "congestion entrada Simon Bolivar",
                                                                         "description" : "congestion en la av. 68, entrada al simon bolivar por evento deportivo",
                                                                         "coord_lat" : lat,
                                                                         "coord_len" : len,
                                                                         "photo" : photo})
        print "Response status code:", response.status_code

    @task(2)
    def get_vias(self):
        response = self.client.get("/vias")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
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
        len_A = randint(-180,180)
        lat_B = randint(-90,90)
        len_B = randint(-180,180)
        response = self.client.post("/vias", {"active":"true",
                                              "name": "AV "+str(number),
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
        response = self.client.get("/places?type="+place_type)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def new_place(self):
        lat = randint(-90,90)
        len = randint(-180,180)
        response = self.client.post("/places", {"type": "tourism",
                                                "name": "Candelaria",
                                                "coord_lat":lat,
                                                "coord_len":len,
                                                "url": "http://lacandelaria.info/",
                                                "photo":"/home/monica/Descargas/contest_winner.jpeg"})
        print "Response status code:", response.status_code

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

    @task(2)
    def get_benefits_by_active(self):
        response = self.client.get("/benefits?active="+benefits_active)
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
        response = self.client.get("/benefits?category="+benefits_category)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(4)
    def get_benefits_by_type(self):
        response = self.client.get("/benefits?type="+benefits_type)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(4)
    def get_benefits_by_cicloviaService(self):
        response = self.client.get("/benefits?cicloviaService="+benefits_cicloviaService)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def new_benefit(self):
        lat = randint(-90,90)
        len = randint(-180,180)
        response = self.client.post("/benefits", {"active":"false",
                                                  "name": "aerobicos Salitre",
                                                  "coord_lat":lat,
                                                  "coord_len":len,
                                                  "category": "service",
                                                  "type": "sport",
                                                  "cicloviaService":"aerobics",
                                                  "description":"sesion de aerobicos para personas mayores de edad",
                                                  "url":"http://www.idrd.gov.co/web/htms/seccion-recreova_1094.html",
                                                  "photo":"/home/monica/Descargas/contest_winner.jpeg"})

        print "Response status code:", response.status_code

    @task(1)
    def get_notifications(self):
        response = self.client.get("/notifications")
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(1)
    def get_notifications_by_id(self):
        response = self.client.get("/notifications?notification_id="+notification_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_notifications_active(self):
        response = self.client.get("/notifications?active="+notification_active)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_notifications_type(self):
        response = self.client.get("/notifications?type="+notification_type)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def get_notifications_priority(self):
        response = self.client.get("/notifications?priority="+notification_priority)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

    @task(2)
    def new_notifications(self):
        lat = randint(-90,90)
        len = randint(-180,180)
        response = self.client.post("/notifications", {"active":"false",
                                                       "type":"news",
                                                       "priority":"low",
                                                       "message":"sesion de aerobicos",
                                                       "url":"http://www.idrd.gov.co/web/htms/seccion-recreova_1094.html",
                                                       "photo":"/home/monica/Descargas/contest_winner.jpeg"})
        print "Response status code:", response.status_code


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000