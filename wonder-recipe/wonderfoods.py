import requests
from secrets import API_KEY
from cuisinesdiets import cuisines

class WonderFood:

    def __init__(self, apiKey, cuisine, number):
        self.apiKey = apiKey
        self.cuisine = cuisine
        self.number = number

    def serialize(self):
        CUISINE_URL = 'https://api.spoonacular.com/recipes/complexSearch/'
        cuisine_payload = {'apiKey': self.apiKey, 'cuisine': self.cuisine, 'number': self.number}
        response_cuisine = requests.get(CUISINE_URL, params=cuisine_payload)

        # information_payload = {'apiKey': self.apiKey, 'includeNutrition': False}
        # INFORMATION_URL = f'https://api.spoonacular.com/recipes/716268/information/'
        # response_information = requests.get(INFORMATION_URL, params=information_payload)

        # print("******", response_cuisine["extendedIngredients"].text)

        # print("******", response_cuisine.text)

        cuisine_json_response = response_cuisine.json()

        cuisine_dictionary = {}
        cuisine_list = []

        for response in cuisine_json_response["results"]:
            cuisine_dictionary["id"] = response["id"]
            cuisine_dictionary["title"] = response["title"]
            cuisine_dictionary["image"] = response["image"]
            cuisine_dictionary["cuisine"] = self.cuisine

            information_payload = {'apiKey': self.apiKey, 'includeNutrition': False}
            INFORMATION_URL = f'https://api.spoonacular.com/recipes/{response["id"]}/information/'
            response_information = requests.get(INFORMATION_URL, params=information_payload)
            information_json_response = response_information.json()

            cuisine_dictionary["readyInMinutes"] = information_json_response["readyInMinutes"]
            
            cuisine_dictionary_copy = cuisine_dictionary.copy()
            cuisine_list.append(cuisine_dictionary_copy)

        return cuisine_list

    def __repr__(self):
        return f'<Wonder Food {self.apiKey} cuisine={self.cuisine} number={self.number}>'

foods = WonderFood(apiKey=API_KEY, cuisine='african', number=1)
print(foods.serialize())
# food_list = []
# for cuisine in cuisines:
#     foods = WonderFood(apiKey=API_KEY, cuisine=cuisine, number=1)
#     print(foods.serialize())
#     print('***************before***************', foods.serialize())
# print('***************after***************', foods.serialize())
# response_json = jsonify(food_list)

# return (response_json, 200)