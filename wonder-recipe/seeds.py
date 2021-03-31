""""Seed file to make sample data for wonder recipes db."""

from models import *
from app import app
from cuisinesdiets import cuisines, diets
from secrets import API_KEY
from wonderrecipes import WonderRecipe
import requests

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Cuisine.query.delete()
Diet.query.delete()
Recipe.query.delete()
RecipeDiet.query.delete()
GroceryList.query.delete()
Likes.query.delete()

# Add users
lawrence = User(username='lawrence123', email='lawrence@gmail.com', password='abc123', phone_number='6105791888')
julie = User(username='julie1', email='julie@gmail.com', password='123abc', phone_number='6105791885')
miguel = User(username='miguel91', email='miguel@gmail.com', password='00123', phone_number='6105791845')

# Add cuisine
cuisine_list = []
for cuisine in cuisines:
   add_cuisine = Cuisine(title=cuisine)
   cuisine_list.append(add_cuisine)

# Add diet
diet_list = []
for diet in diets:
   add_diet = Diet(title=diet)
   diet_list.append(add_diet)

# Adds new User, Cuisine, Diet objects
db.session.add_all([lawrence, julie, miguel])
db.session.add_all(cuisine_list)
db.session.add_all(diet_list)
db.session.commit()

# Adds Recipe after Cuisine has been made to link the relationship
# between Recipe and Cuisine
####################################
# recipe_list = []
# for cuisine in cuisines:
#    recipes = WonderRecipe(apiKey=API_KEY, cuisine=cuisine, number=1)
#    serialized_recipes = recipes.serialize()
#    for index, item in enumerate(serialized_recipes):
#       title = serialized_recipes[index]["title"]
#       image = serialized_recipes[index]["image"]
#       ingredients = serialized_recipes[index]["ingredients"]
#       directions = serialized_recipes[index]["directions"]
#       ready_in_minutes = serialized_recipes[index]["readyInMinutes"]
#       servings = serialized_recipes[index]["servings"]
#       cuisine_id = Cuisine.query.filter(Cuisine.title == cuisine).first().id

#       recipe = Recipe(title=title, image=image, ingredients=ingredients, directions=directions, ready_in_minutes=ready_in_minutes, servings=servings, cuisine_id=cuisine_id)
#       recipe_list.append(recipe)

# db.session.add_all(recipe_list)
# db.session.commit()

# Adds Recipe and Diet for M:M relationship
####################################
# recipe_diet_list = []
# recipes = Recipe.query.all()
# diets = Diet.query.all()

# for recipe_diet in recipes:
CUISINE_URL = 'https://api.spoonacular.com/recipes/complexSearch/'
cuisine_payload = {'apiKey': API_KEY, 'cuisine': 'african', 'number': 1, 'addRecipeInformation': True}
response_cuisine = requests.get(CUISINE_URL, params=cuisine_payload)

cuisine_json_response = response_cuisine.json()

for response in cuisine_json_response["results"]:
   for diet in response["diets"]:
      print(diet)
   # diets = response["diets"][0]
# pancake_vegan = RecipeDiet(recipe_id=1234, diet_id=1)
# pancake_vegetarian = RecipeDiet(recipe_id=1234, diet_id=2)

# Add Grocery List
####################################
# lawrence_burger = GroceryList(user_id=1, recipe_id=4321)
# lawrence_pancake = GroceryList(user_id=1, recipe_id=1234)
# julie_burger = GroceryList(user_id=2, recipe_id=4321)

# Add Likes
####################################
# julie_pancake = Likes(user_id=2, recipe_id=1234)
# miguel_burger = Likes(user_id=3, recipe_id=4321)

# Adds Recipe and Diet M:M relationship after Recipe and Diet
# Tables have been made
####################################
# db.session.add_all([pancake_vegan, pancake_vegetarian])
# db.session.commit()

# Adds Grocery List, Likes
####################################
# db.session.add_all([lawrence_burger, lawrence_pancake, julie_burger])
# db.session.add_all([julie_pancake, miguel_burger])
# db.session.commit()