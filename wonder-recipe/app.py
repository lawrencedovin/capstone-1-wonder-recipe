from flask import Flask, request, render_template, redirect, flash, jsonify, session, g
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func, select
from wonderrecipes import WonderRecipe
from secrets import API_KEY
from cuisinesdiets import cuisines
from models import *
from forms import RegisterForm, LoginForm, EditForm
from random import sample
import operator
from functions import search_diet_filter, search_cuisine_filter

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wonder_recipe_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'pikachu'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# @app.before_request decorator allows us to create a function 
# that will run before each request. Before each page loads when being
# directed to a route it sets the global user variable to the current user in session
# If there's no session/ user is not logged in then g.user is set to None.
# Performs the function before being redirected
@app.before_request
def add_user_to_g():
    """If we're logged in, add current user to Flask global."""

    if CURR_USER_KEY in session:
        # session is carried across request/ per client data while g is per requested data
        # g exists across all of your request, the data is not transferred over like a session between requests 
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def home():
    recipes = Recipe.query.filter().order_by(func.random()).limit(24).all()
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url
    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/<int:user_id>/liked_recipes')
def liked_recipes(user_id):

    recipes = g.user.liked_recipes[:24]
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")
    
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    url = request.url
    
    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/<int:user_id>/grocery_list')
def grocery_list(user_id):

    recipes = g.user.grocery_list_recipes[:24]
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")
    
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/recipe/<int:recipe_id>')
def recipe_page(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/users/add_like/<int:recipe_id>', methods=['POST'])
def add_like(recipe_id):
    """Add a like for a recipe"""

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")

    liked_recipe = Recipe.query.get_or_404(recipe_id)
    g.user.liked_recipes.append(liked_recipe)
    db.session.commit()

    # request.referrer sends user to previous page :)
    return redirect(request.referrer)

@app.route('/users/remove_like/<int:recipe_id>', methods=['POST'])
def remove_like(recipe_id):
    """Remove a like for a recipe"""

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")

    liked_recipe = Recipe.query.get_or_404(recipe_id)
    g.user.liked_recipes.remove(liked_recipe)
    db.session.commit()

    # request.referrer sends user to previous page :)
    return redirect(request.referrer)

@app.route('/users/add_grocery_item/<int:recipe_id>', methods=['POST'])
def add_grocery_item(recipe_id):
    """Add an item for grocery list"""

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")

    grocery_item = Recipe.query.get_or_404(recipe_id)
    g.user.grocery_list_recipes.append(grocery_item)
    db.session.commit()

    # request.referrer sends user to previous page :)
    return redirect(request.referrer)

@app.route('/users/remove_grocery_item/<int:recipe_id>', methods=['POST'])
def remove_grocery_item(recipe_id):
    """Remove an item like for grocery list """

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")

    grocery_item = Recipe.query.get_or_404(recipe_id)
    g.user.grocery_list_recipes.remove(grocery_item)
    db.session.commit()

    # request.referrer sends user to previous page :)
    return redirect(request.referrer)

# Filtering Homepage

@app.route('/diets/<search_diet>')
def diet_search(search_diet):

    all_recipes = Recipe.query.all()
    recipes = search_diet_filter(all_recipes, search_diet)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/cuisines/<search_cuisine>')
def cuisine_search(search_cuisine):

    all_recipes = Recipe.query.all()
    recipes = search_cuisine_filter(all_recipes, search_cuisine)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

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
    
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/likes_descending')
def search_descending_likes():
    """Page that displays 24 recipes by likes
    in descending order.    
    """

    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in Recipe.query.all():
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by descending order, the key,value pairs with the highest
    # likes will go first.
    descending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1), reverse=True))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    descending_likes_recipe_list = []
    for key, value in descending_order.items():
        descending_likes_recipe_list.append(Recipe.query.get(key))

    recipes = descending_likes_recipe_list[:24]

    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/likes_ascending')
def search_ascending_likes():
    """Page that displays 24 recipes by likes
    in ascending order.    
    """

    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in Recipe.query.all():
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by ascending order, the key,value pairs with the highest
    # likes will go first.
    ascending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1)))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    ascending_likes_recipe_list = []
    for key, value in ascending_order.items():
        ascending_likes_recipe_list.append(Recipe.query.get(key))

    recipes = ascending_likes_recipe_list[:24]

    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)


# Filtering Likes
@app.route('/users/liked_recipes/diets/<search_diet>')
def user_liked_recipe_diet_search(search_diet):

    all_recipes = g.user.liked_recipes[:24]
    recipes = search_diet_filter(all_recipes, search_diet)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/cuisines/<search_cuisine>')
def user_liked_recipe_cuisine_search(search_cuisine):

    all_recipes = g.user.liked_recipes[:24]
    recipes = search_cuisine_filter(all_recipes, search_cuisine)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/grocery_list/diets/<search_diet>')
def user_grocery_list_diet_search(search_diet):

    all_recipes = g.user.grocery_list_recipes[:24]
    recipes = search_diet_filter(all_recipes, search_diet)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/grocery_list/cuisines/<search_cuisine>')
def user_grocery_list_cuisine_search(search_cuisine):

    all_recipes = g.user.grocery_list_recipes[:24]
    recipes = search_cuisine_filter(all_recipes, search_cuisine)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/search')
def user_liked_recipe_search_recipes():
    """Page with listing of recipes.
    Can take a 'q' param in querystring to search by that recipe name.
    """

    search = request.args.get('q')
    recipes_list = []

    if not search:
        recipes = g.user.liked_recipes[:24]
    else:
        recipes = Recipe.query.filter(Recipe.title.like(f"%{search.capitalize()}%")).all()
        for recipe in recipes:
            if recipe in g.user.liked_recipes:
                recipes_list.append(recipe)
        recipes = recipes_list[:24]

    
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/grocery_list/search')
def user_grocery_list_search_recipes():
    """Page with listing of recipes.
    Can take a 'q' param in querystring to search by that recipe name.
    """

    search = request.args.get('q')
    recipes_list = []

    if not search:
        recipes = g.user.grocery_list_recipes[:24]
    else:
        recipes = Recipe.query.filter(Recipe.title.like(f"%{search.capitalize()}%")).all()
        for recipe in recipes:
            if recipe in g.user.grocery_list_recipes:
                recipes_list.append(recipe)
        recipes = recipes_list[:24]
    
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/likes_descending')
def user_liked_recipes_descending_likes():
    """Page that displays 24 recipes by likes
    in descending order.    
    """

    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in g.user.liked_recipes:
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by descending order, the key,value pairs with the highest
    # likes will go first.
    descending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1), reverse=True))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    descending_likes_recipe_list = []
    for key, value in descending_order.items():
        descending_likes_recipe_list.append(Recipe.query.get(key))

    recipes = descending_likes_recipe_list[:24]

    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/likes_ascending')
def user_liked_ascending_likes():
    """Page that displays 24 recipes by likes
    in ascending order.    
    """

    # Makes dictionary out of id as the key and likes as of value ie. {1231234: 1}
    recipe_dict = {}
    for recipe in Recipe.query.all():
        recipe_dict[recipe.id] = len(recipe.liked_by_users)

    # Sorts dictionary by ascending order, the key,value pairs with the highest
    # likes will go first.
    ascending_order = dict(sorted(recipe_dict.items(), key=operator.itemgetter(1)))

    # Stores the full recipes by getting the id and places it
    # into a list based on the sorted dictionary
    ascending_likes_recipe_list = []
    for key, value in ascending_order.items():
        ascending_likes_recipe_list.append(Recipe.query.get(key))

    recipes = ascending_likes_recipe_list[:24]

    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

# Filtering Grocery List

# Forms
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Added User"""

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                phone_number=form.phone_number.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)

        # if validated sets session[CURR_USER_KEY] = user.id before redirecting
        do_login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            # if validated sets session[CURR_USER_KEY] = user.id before redirecting
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/verify_account')
def verify_account():
    return render_template('verify-account.html')

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit-profile.html')

# Logout
@app.route('/logout')
def logout():
    """Handle logout of user."""

    # IMPLEMENT THIS
    do_logout()
    flash('Logged out successfully', 'success')
    return redirect('/')

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