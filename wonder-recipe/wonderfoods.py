import requests

class WonderFood:

    def __init__(self, apiKey, cuisine, number):
        self.apiKey = apiKey
        self.cuisine = cuisine
        self.number = number

    def serialize(self):
        payload = {'apiKey': self.apiKey, 'cuisine': self.cuisine, 'number': self.number}
        response_wonder_food = requests.get('https://api.spoonacular.com/recipes/complexSearch/', params=payload)
        # print(response_wonder_food.text)

        json_response = response_wonder_food.json()

        food_dictionary = {}
        food_list = []

        for response in json_response["results"]:
            food_dictionary["id"] = response["id"]
            food_dictionary["title"] = response["title"]
            food_dictionary["image"] = response["image"]
            food_dictionary["cuisine"] = self.cuisine
            
            food_dictionary_copy = food_dictionary.copy()
            food_list.append(food_dictionary_copy)

        return food_list

    def __repr__(self):
        return f'<Wonder Food {self.apiKey} cuisine={self.cuisine} number={self.number}>'