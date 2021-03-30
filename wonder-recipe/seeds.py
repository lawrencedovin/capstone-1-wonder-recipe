""""Seed file to make sample data for wonder recipes db."""

from models import *
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Cuisine.query.delete()
Diet.query.delete()
# PostTag.query.delete()

# Add users
lawrence = User(username='lawrence123', email='lawrence@gmail.com', password='abc123', phone_number='6105791888')
julie = User(username='julie1', email='julie@gmail.com', password='123abc', phone_number='6105791885')
miguel = User(username='miguel91', email='miguel@gmail.com', password='00123', phone_number='6105791845')

# Add cuisine
african = Cuisine(cuisine_name='african')
greek = Cuisine(cuisine_name='greek')

# Add diet
vegan = Diet(diet_name='vegan')
vegetarian = Diet(diet_name='vegetarian')

# Add recipe
pancake = Recipe(id=1234, recipe_name='pancakes', 
        ingredients=[
         {
            "name":"bell peppers",
            "amount":1.0,
            "unit":"serving"
         }
      ],
      directions=[
         {
            "number":1,
            "step":"Season and Boil the Chicken for 10 minutes with salt, pepper, and seasoning."
         }
      ],
      ready_in_minutes=45,
      servings=1,
      cuisine_id=1)

burger = Recipe(id=4321, recipe_name='burger', 
        ingredients=[
         {
            "name":"burger patty",
            "amount":1.0,
            "unit":"slice"
         }
      ],
      directions=[
         {
            "number":1,
            "step":"Add Patty on buns and then cheese."
         }
      ],
      ready_in_minutes=25,
      servings=1,
      cuisine_id=2)

# Adds Recipe and Diet for M:M relationship
pancake_vegan = RecipeDiet(recipe_id=1234, diet_id=1)
pancake_vegetarian = RecipeDiet(recipe_id=1234, diet_id=2)

# Add Grocery List
lawrence_burger = GroceryList(user_id=1, recipe_id=4321)
lawrence_pancake = GroceryList(user_id=1, recipe_id=1234)
julie_burger = GroceryList(user_id=2, recipe_id=4321)

# Add new object to session, so they'll persist
db.session.add_all([lawrence, julie, miguel])
db.session.add_all([african, greek])
db.session.add_all([vegan, vegetarian])

# Commit confirms changes and makes it permanent
db.session.commit()

# Adds Recipe after Cuisine has been made to link the relationship
# between Recipe and Cuisine
db.session.add_all([pancake])
db.session.commit()

# Adds Recipe and Diet M:M relationship after Recipe and Diet
# Tables have been made
db.session.add_all([pancake_vegan, pancake_vegetarian])
db.session.commit()

# Adds Grocery List, Liked Recipes, Likes
db.session.add_all([lawrence_burger, lawrence_pancake, julie_burger])
db.session.commit()

