from random import sample
import operator
from models import *

def search_diet_filter(all_recipes, search_diet):
    # Searches for which recipe contains the diet
    # in their recipe.diets list then adds it to list

    recipes = []
    for recipe in all_recipes:
        for diet in recipe.diets:
            if(diet.title == search_diet):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes
    return recipes

def search_cuisine_filter(all_recipes, search_cuisine):
    # Searches for which recipe contains the cuisine
    # in their recipe.cuisines list then adds it to list

    recipes = []
    for recipe in all_recipes:
        for cuisine in recipe.cuisines:
            if(cuisine.title == search_cuisine):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes
    return recipes

def search_likes_descending(user_list):
    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in user_list:
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by descending order, the key,value pairs with the highest
    # likes will go first.
    descending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1), reverse=True))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    descending_likes_recipe_list = []
    for key, value in descending_order.items():
        descending_likes_recipe_list.append(Recipe.query.get(key))

    return descending_likes_recipe_list[:24]

def search_likes_ascending(user_list):
    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in user_list:
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by ascending order, the key,value pairs with the highest
    # likes will go first.
    ascending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1)))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    ascending_likes_recipe_list = []
    for key, value in ascending_order.items():
        ascending_likes_recipe_list.append(Recipe.query.get(key))

    return ascending_likes_recipe_list[:24]

def searchbar(search, user_list):

    recipes_list = []

    if not search:
        recipes = user_list[:24]
    else:
        recipes = Recipe.query.filter(Recipe.title.like(f"%{search.capitalize()}%")).all()
        for recipe in recipes:
            if recipe in user_list:
                recipes_list.append(recipe)
        return recipes_list[:24]