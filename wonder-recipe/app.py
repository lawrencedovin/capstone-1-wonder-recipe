from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from wonderrecipes import WonderRecipe
from secrets import API_KEY
from cuisinesdiets import cuisines
from models import *
from  sqlalchemy.sql.expression import func, select
from random import sample

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wonder_recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'pikachu'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    recipes = Recipe.query.filter().order_by(func.random()).limit(24).all()
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines)

@app.route('/home/logged_in')
def home_logged_in():
    recipes = Recipe.query.filter().order_by(func.random()).limit(24).all()
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    return render_template('home-logged-in.html', recipes=recipes, diets=diets, cuisines=cuisines)

@app.route('/liked_recipes')
def liked_recipes():
    return render_template('liked-recipes.html')

@app.route('/grocery_list')
def grocery_list():
    return render_template('grocery-list.html')

@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return render_template('recipe.html', recipe=recipe)

# Filtering

@app.route('/diets/<search_diet>')
def diet_search(search_diet):
    recipes = []
    all_recipes = Recipe.query.all()
    
    # Searches for which recipe contains the diet
    # in their recipe.diets list then adds it to list

    for recipe in all_recipes:
        for diet in recipe.diets:
            if(diet.title == search_diet):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes

    diets = Diet.query.limit(12).all()
    cuisines = Cuisine.query.all()
    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines)

@app.route('/cuisines/<search_cuisine>')
def cuisine_search(search_cuisine):
    recipes = []
    all_recipes = Recipe.query.all()
    
    # Searches for which recipe contains the cuisine
    # in their recipe.cuisines list then adds it to list

    for recipe in all_recipes:
        for cuisine in recipe.cuisines:
            if(cuisine.title == search_cuisine):
                recipes.append(recipe)
    recipes = sample(recipes, 24) if len(recipes) >= 24 else recipes

    diets = Diet.query.limit(12).all()
    cuisines = Cuisine.query.all()
    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines)

@app.route('/search')
def search_recipes():
    """Page with listing of recipes.
    Can take a 'q' param in querystring to search by that recipe name.
    """

    search = request.args.get('q')

    if not search:
        recipes = Recipe.query.filter().order_by(func.random()).limit(24).all()
    else:
        recipes = Recipe.query.filter(Recipe.title.like(f"%{search.capitalize()}%")).limit(24).all()
    
    diets = Diet.query.limit(12).all()
    cuisines = Cuisine.query.all()

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines) 

# Forms
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verify_account')
def verify_account():
    return render_template('verify-account.html')

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit-profile.html')

# @app.route('/api/get-food', methods=["GET"])
# def get_food():
#     food_list = []
#     for cuisine in cuisines:
#         foods = WonderFood(apiKey=API_KEY, cuisine=cuisine, number=1)
#         print(foods.serialize())
#         # food_list = food_list + foods.serialize()
#         print('***************before***************', foods.serialize())
    
#     # response_json = jsonify(foods.serialize())
#     print('***************after***************', foods.serialize())
#     response_json = jsonify(food_list)

#     return (response_json, 200)

    # [
    #     {cuisine: vietnamese},
    #     .
    #     .
    #     .
    #     {cuisine: chinese}
    # ]
    # [
    #     {cuisine: vietnamese},
    #     {cuisine: vietnamese},

    # ]
    # [
    #     {cuisine: chinese}
    # ]