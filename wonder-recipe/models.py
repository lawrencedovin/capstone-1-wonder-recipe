from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, JSONB

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                     nullable=False)
    email = db.Column(db.String(64),
                     nullable=False)
    password = db.Column(db.String(128),
                     nullable=False)
    phone_number = db.Column(db.String(16),
                     nullable=False)

    def __repr__(self):
        user = self
        return f'<User - id: {user.id} username: {user.username} email: {user.email} password: {user.password} phone_number: {user.phone_number}>'

class Cuisine(db.Model):
    __tablename__ = 'cuisines'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    cuisine_name = db.Column(db.String(64),
                     nullable=False)

    def __repr__(self):
        cuisine = self
        return f'<Cuisine - id: {cuisine.id} cuisine_name: {cuisine.cuisine_name}>'

class Diet(db.Model):
    __tablename__ = 'diets'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    diet_name = db.Column(db.String(64),
                     nullable=False)

    def __repr__(self):
        diet = self
        return f'<Diet - id: {diet.id} diet_name: {diet.diet_name}>'

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer,
                   primary_key=True)
    recipe_name = db.Column(db.String(64),
                     nullable=False)
    ingredients = db.Column(JSONB,
                     nullable=False)
    directions = db.Column(JSONB,
                     nullable=False)
    ready_in_minutes = db.Column(db.Numeric(scale=2, asdecimal=False))
    servings = db.Column(db.Numeric(scale=2, asdecimal=False))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.id'))

    cuisine = db.relationship('Cuisine', backref='recipes')

    def __repr__(self):
        recipe = self
        return f'<Recipe - id: {recipe.id} recipe_name: {recipe.recipe_name} ingredients: {recipe.ingredients} directions: {recipe.directions} ready_in_minutes: {recipe.ready_in_minutes} servings: {recipe.servings} cuisine_id: {recipe.cuisine_id}>'

class RecipeDiet(db.Model):
    __tablename__ = 'recipe_diet'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.id'), primary_key=True)

    def __repr__(self):
        recipe_diet = self
        return f'<Recipe Diet - recipe_id: {recipe_diet.recipe_id} diet_id: {recipe_diet.diet_id}>'

class GroceryList(db.Model):
    __tablename__ = 'grocery_list'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)

    def __repr__(self):
        grocery_list = self
        return f'<Grocery List - user_id: {grocery_list.user_id} recipe_id: {grocery_list.recipe_id}>'

class LikedRecipes(db.Model):
    __tablename__ = 'liked_recipes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)

    def __repr__(self):
        liked_recipes = self
        return f'<Liked Recipes - user_id: {liked_recipes.user_id} recipe_id: {liked_recipes.recipe_id}>'

class Likes(db.Model):
    __tablename__ = 'likes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)

    def __repr__(self):
        likes = self
        return f'<Likes - user_id: {likes.user_id} recipe_id: {likes.recipe_id}>'
