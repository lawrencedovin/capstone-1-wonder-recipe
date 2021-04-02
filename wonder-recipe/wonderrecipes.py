import requests
from secrets import API_KEY
from cuisinesdiets import cuisines
from unicodedata import normalize

class WonderRecipe:

    def __init__(self, apiKey, cuisine, number):
        self.apiKey = apiKey
        self.cuisine = cuisine
        self.number = number

    def serialize(self):
        CUISINE_URL = 'https://api.spoonacular.com/recipes/complexSearch/'
        cuisine_payload = {'apiKey': self.apiKey, 'cuisine': self.cuisine, 'number': self.number, 'addRecipeInformation': True, 'addRecipeNutrition': True}
        response_cuisine = requests.get(CUISINE_URL, params=cuisine_payload)

        cuisine_json_response = response_cuisine.json()

        food_dictionary = {}
        food_list = []

        for response in cuisine_json_response["results"]:
            food_dictionary["id"] = response["id"]
            food_dictionary["title"] = response["title"]
            food_dictionary["image"] = response["image"]
            food_dictionary["cuisine"] = self.cuisine

            # Checks if steps are found in the directions json response
            # Otherwise set to default values
            # try:
            #     for nutrient in response[0]["nutrition"]:
            # #         print(nutrient)
            # #         directions_dictionary["number"] = direction["number"]
            # #         # normalize is used to replace \xa0 with spaces in step string
            # #         directions_dictionary["step"] = normalize("NFKD", direction["step"])

            # #         directions_dictionary_copy = directions_dictionary.copy()
            # #         food_dictionary["directions"].append(directions_dictionary_copy)
            # # except:
            #     peanuts = 1

            # Information API Call
            information_payload = {'apiKey': self.apiKey, 'includeNutrition': False}
            INFORMATION_URL = f'https://api.spoonacular.com/recipes/{response["id"]}/information/'
            response_information = requests.get(INFORMATION_URL, params=information_payload)
            information_json_response = response_information.json()
        
            food_dictionary["readyInMinutes"] = information_json_response["readyInMinutes"]
            food_dictionary["servings"] = information_json_response["servings"]
            food_dictionary["diets"] = response["diets"]

            ingredients_dictionary = {}
            food_dictionary["ingredients"] = []
            ingredients_dictionary["name"] = ''
            ingredients_dictionary["amount"] = ''
            ingredients_dictionary["unit"] = ''

            for ingredient in information_json_response["extendedIngredients"]:
                ingredients_dictionary["name"] = ingredient["name"] 
                ingredients_dictionary["amount"] = ingredient["amount"] 
                ingredients_dictionary["unit"] = ingredient["unit"] 

                ingredients_dictionary_copy = ingredients_dictionary.copy()
                food_dictionary["ingredients"].append(ingredients_dictionary_copy)

            # Directions API Call
            directions_payload = {'apiKey': self.apiKey}
            DIRECTIONS_URL = f'https://api.spoonacular.com/recipes/{response["id"]}/analyzedInstructions/'
            response_directions = requests.get(DIRECTIONS_URL, params=directions_payload)
            directions_json_response = response_directions.json()
            directions_dictionary = {}
            food_dictionary["directions"] = []

            directions_dictionary["number"] = ''
            directions_dictionary["step"] = ''

            # Checks if steps are found in the directions json response
            # Otherwise set to default values
            try:
                for direction in directions_json_response[0]["steps"]:
                    directions_dictionary["number"] = direction["number"]
                    # normalize is used to replace \xa0 with spaces in step string
                    directions_dictionary["step"] = normalize("NFKD", direction["step"])

                    directions_dictionary_copy = directions_dictionary.copy()
                    food_dictionary["directions"].append(directions_dictionary_copy)
            except:
                # print("Steps not found")
                peanuts = 1

            food_dictionary_copy = food_dictionary.copy()
            food_list.append(food_dictionary_copy)

        return food_list

    def __repr__(self):
        return f'<Wonder Recipe cuisine={self.cuisine} number={self.number}>'

# recipes = WonderRecipe(apiKey=API_KEY, cuisine='african', number=1)
# serialized_recipes = recipes.serialize()
# print(serialized_recipes)


CUISINE_URL = 'https://api.spoonacular.com/recipes/complexSearch/'
cuisine_payload = {'apiKey': API_KEY, 'cuisine': 'african', 'number': 1, 'addRecipeInformation': True, 'addRecipeNutrition': True}
response_cuisine = requests.get(CUISINE_URL, params=cuisine_payload)
cuisine_json_response = response_cuisine.json()

for response in cuisine_json_response["results"]:
    for nutrient in response["nutrition"]["nutrients"]:
        if nutrient["name"] == "Calories" or nutrient["name"] == "Protein" or nutrient["name"] == "Carbohydrates" or nutrient["name"] == "Fat":
            print(f'name: {nutrient["name"]}')
            print(f'amount: {nutrient["amount"]}')
            print(f'unit: {nutrient["unit"]}')
        # if nutrient["name"] == "Protein":
    # print(response["nutrition"])
# for response in cuisine_json_response["nutrition"]:
#     print(response)
