"""Recipe View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_recipe_views.py


import os
from unittest import TestCase

from models import *

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] =  "postgresql:///wonder_recipe_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

# app.config['WTF_CSRF_ENABLED'] = False