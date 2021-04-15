def search_diet_filter(all_recipes, search_diet):
    recipes = []
    for recipe in all_recipes:
        for diet in recipe.diets:
            if(diet.title == search_diet):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes
    return recipes

def search_cuisine_filter(all_recipes, search_cuisine):
    recipes = []
    for recipe in all_recipes:
        for cuisine in recipe.cuisines:
            if(cuisine.title == search_cuisine):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes
    return recipes