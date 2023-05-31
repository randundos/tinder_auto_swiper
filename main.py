from tinder_api import tinderAPI
from time import sleep
from random import random

PROF_FILE = "./images/unclassified/profiles.txt"

if __name__ == "__main__":
    token = "9c97af71-ec6a-4002-af30-c368d2bb5a83"
    api = tinderAPI(token)

    while True:
        persons = api.nearby_persons()
        for person in persons:
            person.download_images(folder="./images/unclassified", sleep_max_for=random()*3)
            sleep(random()*10)
        sleep(random()*10)
        # person.like()