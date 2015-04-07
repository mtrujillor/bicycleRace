from locust import HttpLocust, TaskSet, task
from random import randint

#test data
user_id = "55230e89bd3cc668fe73131f"
photo = "/home/monica/Descargas/contest_winner.jpeg"


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
    def get_user(self):
        response = self.client.get("/users?user_id="+user_id)
        print "Response status code:", response.status_code
        #print "Response content:", response.content

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


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000