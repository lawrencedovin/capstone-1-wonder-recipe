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

# Add recipe_diet



# Add post tag relationships
# first_fun_tag = PostTag(post_id=1, tag_id=1)
# first_hip_tag = PostTag(post_id=1, tag_id=3)
# puberty_fun_tag = PostTag(post_id=2, tag_id=1)
# puberty_cool_tag = PostTag(post_id=2, tag_id=2)

# Add new object to session, so they'll persist
db.session.add_all([lawrence, julie, miguel])
db.session.add_all([african, greek])
db.session.add_all([vegan, vegetarian])
# db.session.add_all([post1, post2])
# db.session.add_all([fun_tag, cool_tag, hip_tag, fancy_tag])

# Commit confirms changes and makes it permanent
db.session.commit()

# Add post to tag relationship after initial data has been entered
db.session.add_all([pancake])
db.session.commit()