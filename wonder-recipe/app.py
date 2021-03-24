from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from wonderfoods import WonderFood
from secrets import API_KEY
from cuisinesdiets import cuisines

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = False
toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home/logged_in')
def home_logged_in():
    return render_template('home-logged-in.html')

@app.route('/liked_recipes')
def liked_recipes():
    return render_template('liked-recipes.html')

@app.route('/grocery_list')
def grocery_list():
    return render_template('grocery-list.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe-page.html')

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
