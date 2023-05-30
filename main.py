from tinder_api import tinderAPI

if __name__ == "__main__":
    token = "YOUR-API-TOKEN"
    api = tinderAPI(token)

    while True:
        persons = api.nearby_persons()
        for person in persons:
            print(person)
            # person.like()