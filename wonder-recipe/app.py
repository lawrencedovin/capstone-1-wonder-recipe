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
from functions import *

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///wonder_recipe'
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

# Homepage

@app.route('/')
def home():
    return redirect("/page_1")

# Pagination
@app.route('/page_<int:page_number>')
def paginate_food(page_number):
    recipes = []
    recipes_paginate = Recipe.query.paginate(page=page_number, per_page=24)
    for recipe in recipes_paginate.items:
        recipes.append(recipe)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url
    if page_number > 5:
        page_list = list(range(page_number-2, page_number+3))
    else:
        page_list = [item for item in range(1, 6)]
    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url, page_number=page_number, page_list=page_list)

# User Pages

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

    recipes = search_likes_descending(Recipe.query.all())
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('home.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/likes_ascending')
def search_ascending_likes():
    """Page that displays 24 recipes by likes
    in ascending order.    
    """

    recipes = search_likes_ascending(Recipe.query.all())
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

@app.route('/users/liked_recipes/search')
def user_liked_recipe_search_recipes():
    """Page with listing of recipes.
    Can take a 'q' param in querystring to search by that recipe name.
    """

    search = request.args.get('q')
    recipes = searchbar(search, g.user.liked_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/likes_descending')
def user_liked_recipes_descending_likes():
    """Page that displays 24 recipes by likes
    in descending order.    
    """

    recipes = search_likes_descending(g.user.liked_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/liked_recipes/likes_ascending')
def user_liked_recipes_ascending_likes():
    """Page that displays 24 recipes by likes
    in ascending order.    
    """

    recipes = search_likes_ascending(g.user.liked_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('liked-recipes.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

# Filtering Grocery List
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

@app.route('/users/grocery_list/search')
def user_grocery_list_search_recipes():
    """Page with listing of recipes.
    Can take a 'q' param in querystring to search by that recipe name.
    """

    search = request.args.get('q')
    recipes = searchbar(search, g.user.grocery_list_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/grocery_list/likes_descending')
def user_grocery_list_descending_likes():
    """Page that displays 24 recipes by likes
    in descending order.    
    """

    recipes = search_likes_descending(g.user.grocery_list_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

@app.route('/users/grocery_list/likes_ascending')
def user_grocery_list_ascending_likes():
    """Page that displays 24 recipes by likes
    in ascending order.    
    """

    recipes = search_likes_ascending(g.user.grocery_list_recipes)
    diets = Diet.query.limit(11).all()
    cuisines = Cuisine.query.all()
    url = request.url

    return render_template('grocery-list.html', recipes=recipes, diets=diets, cuisines=cuisines, url=url)

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

@app.route('/users/edit_profile', methods=["GET", "POST"])
def edit_profile():
    """Updated profile for current user."""

    if not g.user:
        flash("Login to your account.", "danger")
        return redirect("/")
    
    user = g.user
    form = EditForm(obj=user)

    if form.validate_on_submit():

        if User.authenticate(user.username, form.password.data):

            try:
                user.username = form.username.data
                user.email = form.email.data
                user.phone_number = form.phone_number.data

                db.session.commit()
            
            except IntegrityError:
                flash('Username or Email Address is already taken', 'danger')
                db.session.rollback()
                return redirect('/users/edit_profile')
            
            flash(f'{user.username} successfully updated!', 'form-success')
            return redirect('/users/edit_profile')
        else:
            flash('Invalid Password', 'danger')
            return redirect('/users/edit_profile')
        
    else:
        return render_template('edit-profile.html', user=user, form=form)

# Logout
@app.route('/logout')
def logout():
    """Handle logout of user."""

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