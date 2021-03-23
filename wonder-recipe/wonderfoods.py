import requests

class WonderFood:

    def __init__(self, apiKey, cuisine, number):
        self.apiKey = apiKey
        self.cuisine = cuisine
        self.number = number

    def serialize(self):
        payload = {'apiKey': self.apiKey, 'cuisine': self.cuisine, 'number': self.number}
        response_wonder_food = requests.get('https://api.spoonacular.com/recipes/complexSearch/', params=payload)
        print(response_wonder_food.text)

        return {
            "data": response_wonder_food.text,
            "cuisine": self.cuisine
        }

    def __repr__(self):
        return f'<Wonder Food {self.apiKey} cuisine={self.cuisine} number={self.number}>'