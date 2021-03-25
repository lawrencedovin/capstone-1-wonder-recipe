import requests
from secrets import API_KEY
from cuisinesdiets import cuisines
from unicodedata import normalize

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

        food_dictionary = {}
        food_list = []

        for response in cuisine_json_response["results"]:
            food_dictionary["id"] = response["id"]
            food_dictionary["title"] = response["title"]
            food_dictionary["image"] = response["image"]
            food_dictionary["cuisine"] = self.cuisine

            # Information API Call
            information_payload = {'apiKey': self.apiKey, 'includeNutrition': False}
            INFORMATION_URL = f'https://api.spoonacular.com/recipes/{response["id"]}/information/'
            response_information = requests.get(INFORMATION_URL, params=information_payload)
            information_json_response = response_information.json()
        
            food_dictionary["readyInMinutes"] = information_json_response["readyInMinutes"]
            food_dictionary["servings"] = information_json_response["servings"]

            ingredients_dictionary = {}
            food_dictionary["ingredients"] = []

            for ingredient in information_json_response["extendedIngredients"]:
                ingredients_dictionary["name"] = ingredient["name"] 
                ingredients_dictionary["amount"] = ingredient["amount"] 
                ingredients_dictionary["unit"] = ingredient["unit"] 

                ingredients_dictionary_copy = ingredients_dictionary.copy()
                food_dictionary["ingredients"].append(ingredients_dictionary_copy)

            # Directions API Call
            directions_payload = {'apiKey': self.apiKey}
            INFORMATION_URL = f'https://api.spoonacular.com/recipes/{response["id"]}/analyzedInstructions/'
            response_directions = requests.get(INFORMATION_URL, params=directions_payload)
            directions_json_response = response_directions.json()
            # print(directions_json_response[0]["steps"], "**************")
            directions_dictionary = {}
            food_dictionary["directions"] = []

            for direction in directions_json_response[0]["steps"]:
                directions_dictionary["number"] = direction["number"]
                directions_dictionary["step"] = normalize("NFKD", direction["step"])

                directions_dictionary_copy = directions_dictionary.copy()
                food_dictionary["directions"].append(directions_dictionary_copy)


            
            # food_dictionary["ingredients"] = information_json_response["extendedIngredients"]
            
            food_dictionary_copy = food_dictionary.copy()
            food_list.append(food_dictionary_copy)

        return food_list

    def __repr__(self):
        return f'<Wonder Food {self.apiKey} cuisine={self.cuisine} number={self.number}>'

# for cuisine in cuisines:
foods = WonderFood(apiKey=API_KEY, cuisine='african', number=1)
# foods = WonderFood(apiKey=API_KEY, cuisine=cuisine, number=1)
print(foods.serialize())
# food_list = []
# for cuisine in cuisines:
#     foods = WonderFood(apiKey=API_KEY, cuisine=cuisine, number=1)
#     print(foods.serialize())
#     print('***************before***************', foods.serialize())
# print('***************after***************', foods.serialize())
# response_json = jsonify(food_list)

# return (response_json, 200)