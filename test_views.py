"""View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_views.py


import os
from unittest import TestCase

# from models import db, connect_db, Message, User, Likes, Follows
from models import *
# from bs4 import BeautifulSoup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///wonder_recipe_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

# app.config['WTF_CSRF_ENABLED'] = False

class ViewsTestCase(TestCase):
    def test_home_view(self):
        with app.test_client() as client:
            res = client.get('/page_1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="hero-container__caption text-center">Discover Recipes.</h1>', html)
    
    def test_diet_filter_view(self):
        with app.test_client() as client:
            res = client.get('/diets/vegan/page_1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Mushroom Hummus Crostini', html)

    def test_cuisines_filter_view(self):
        with app.test_client() as client:
            res = client.get('/cuisines/mexican/page_1')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Beef Fajita Marinade', html)

    def test_recipe_page_view(self):
        with app.test_client() as client:
            res = client.get('/recipe/715438')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Mexican Casserole', html)
            self.assertIn('700.7 kcal', html)
            self.assertIn('10.00 oz - cream of chicken soup', html)
            self.assertIn('Heat over to 350 degrees. Take cooled chicken breasts and shred, or cut into bite size pieces.', html)
    
    def test_register_page_view(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Create an account', html)
    
    def test_login_page_view(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Enter your user credentials to login', html)