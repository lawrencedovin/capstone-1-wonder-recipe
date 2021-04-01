""""Seed file to make sample data for wonder recipes db."""

from models import *
from app import app
from cuisinesdiets import cuisines, diets
from secrets import API_KEY
from wonderrecipes import WonderRecipe
import requests
from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import text

# Create all tables
####################################
db.drop_all()
db.create_all()

# If table isn't empty, empty it
####################################
User.query.delete()
Cuisine.query.delete()
Diet.query.delete()
Recipe.query.delete()
RecipeDiet.query.delete()
GroceryList.query.delete()
Likes.query.delete()

# Add users
####################################
lawrence = User(username='lawrence123', email='lawrence@gmail.com', password='abc123', phone_number='6105791888')
julie = User(username='julie1', email='julie@gmail.com', password='123abc', phone_number='6105791885')
miguel = User(username='miguel91', email='miguel@gmail.com', password='00123', phone_number='6105791845')

# Add cuisine
####################################
cuisine_list = []
for cuisine in cuisines:
   add_cuisine = Cuisine(title=cuisine)
   cuisine_list.append(add_cuisine)

# Add diet
####################################
diet_list = []
for diet in diets:
   add_diet = Diet(title=diet)
   diet_list.append(add_diet)

# Adds new User, Cuisine, Diet objects
####################################
db.session.add_all([lawrence, julie, miguel])
db.session.add_all(cuisine_list)
db.session.add_all(diet_list)
db.session.commit()

# Adds Recipe after Cuisine has been made to link the relationship
# between Recipe and Cuisine
####################################
recipe_list = []
for cuisine in cuisines:
   recipes = WonderRecipe(apiKey=API_KEY, cuisine=cuisine, number=1)
   serialized_recipes = recipes.serialize()
   for recipe in serialized_recipes:
      id = recipe["id"]
      title = recipe["title"]
      image = recipe["image"]
      ingredients = recipe["ingredients"]
      directions = recipe["directions"]
      ready_in_minutes = recipe["readyInMinutes"]
      servings = recipe["servings"]
      recipe = Recipe(id=id, title=title, image=image, ingredients=ingredients, directions=directions, ready_in_minutes=ready_in_minutes, servings=servings)
      try:
          db.session.add(recipe)
          db.session.commit()
      except exc.IntegrityError:
          db.session.rollback()

# Adds Recipe and Diet, Recipe and Cuisine for M:M relationship
####################################

for cuisine in cuisines:
   recipes = WonderRecipe(apiKey=API_KEY, cuisine=cuisine, number=1)
   serialized_recipes = recipes.serialize()
   for recipe in serialized_recipes:
      id = recipe["id"]
      title = recipe["title"]
      image = recipe["image"]
      ingredients = recipe["ingredients"]
      directions = recipe["directions"]
      ready_in_minutes = recipe["readyInMinutes"]
      servings = recipe["servings"]
      # Extracts the Cuisine table's id for where the match was found
      # between Cuisine db Table and Recipe API call's cuisine.
      cuisine_id = Cuisine.query.filter(Cuisine.title == cuisine).first().id
      recipe_cuisine = RecipeCuisine(recipe_id=id, cuisine_id=cuisine_id)
      try:
        db.session.add(recipe_cuisine)
        db.session.commit()
      except exc.IntegrityError:
        db.session.rollback()

      for diet in recipe["diets"]:
        # Extracts the Diet table's id for where the match was found
        # between Diets db Table and Recipe API call's diet.
        diet_id = Diet.query.filter(Diet.title == diet).first().id
        recipe_diet = RecipeDiet(recipe_id=id, diet_id=diet_id)
        try:
            db.session.add(recipe_diet)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

# Add Grocery List
####################################
# lawrence_burger = GroceryList(user_id=1, recipe_id=4321)
# lawrence_pancake = GroceryList(user_id=1, recipe_id=1234)
# julie_burger = GroceryList(user_id=2, recipe_id=4321)

# Add Likes
####################################
# julie_pancake = Likes(user_id=2, recipe_id=1234)
# miguel_burger = Likes(user_id=3, recipe_id=4321)

# Adds Grocery List
####################################
# db.session.add_all([lawrence_burger, lawrence_pancake, julie_burger])
# db.session.add_all([julie_pancake, miguel_burger])
# db.session.commit()