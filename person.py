import datetime
import requests
from geopy.geocoders import Nominatim
from time import sleep
from random import random

TINDER_URL = "https://api.gotinder.com"
geolocator = Nominatim(user_agent="tinder_auto_swiper")
PROF_FILE = "./images/unclassified/profiles.txt"

class Person(object):

    def __init__(self, data, api):
        self._api = api

        self.id = data["_id"]
        self.name = data.get("name", "Unknown")

        self.bio = data.get("bio", "")
        self.distance = data.get("distance_mi", 0) / 1.60934

        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            "birth_date", False) else None
        self.gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))

        self.jobs = list(
            map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))

        if data.get("pos", False):
            self.location = geolocator.reverse(f'{data["pos"]["lat"]}, {data["pos"]["lon"]}')


    def __repr__(self):
        return f"{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y')})"


    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)

    def download_images(self, folder=".", sleep_max_for=0):
        with open(PROF_FILE, "r") as f:
            lines = f.readlines()
            if self.id in lines:
                return
        
        with open(PROF_FILE, "a") as f:
            f.write(self.id+"\r\n")
        
        index = -1
        
        for image_url in self.images:
            index += 1
            req = requests.get(image_url, stream=True)
            if req.status_code == 200:
                with open(f"{folder}/{self.id}_{self.name}_{index}.jpeg", "wb") as f:
                    f.write(req.content)
            sleep(random()*sleep_max_for)

class Profile(Person):

    def __init__(self, data, api):

        super().__init__(data["user"], api)

        self.email = data["account"].get("email")
        self.phone_number = data["account"].get("account_phone_number")

        self.age_min = data["user"]["age_filter_min"]
        self.age_max = data["user"]["age_filter_max"]

        self.max_distance = data["user"]["distance_filter"]
        self.gender_filter = ["Male", "Female"][data["user"]["gender_filter"]]