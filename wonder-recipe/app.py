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