from random import sample

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