from flask import Flask, request, render_template, redirect, flash, jsonify
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension

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