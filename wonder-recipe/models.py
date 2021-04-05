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
    title = db.Column(db.String(64),
                     nullable=False)

    def __repr__(self):
        cuisine = self
        return f'<Cuisine - id: {cuisine.id} cuisine_title: {cuisine.title}>'

class Diet(db.Model):
    __tablename__ = 'diets'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(64),
                     nullable=False)

    def __repr__(self):
        diet = self
        return f'<Diet - id: {diet.id} title: {diet.title}>'

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(180),
                     nullable=False)
    image = db.Column(db.String(256),
                     nullable=False)
    ingredients = db.Column(JSONB,
                     nullable=False)
    macros = db.Column(JSONB,
                     nullable=False)
    directions = db.Column(JSONB,
                     nullable=False)
    ready_in_minutes = db.Column(db.Numeric(scale=2, asdecimal=False))
    servings = db.Column(db.Numeric(scale=2, asdecimal=False))

    def __repr__(self):
        recipe = self
        return f'<Recipe - id: {recipe.id} title: {recipe.title} image: {recipe.image} ingredients: {recipe.ingredients} macros: {recipe.macros} directions: {recipe.directions} ready_in_minutes: {recipe.ready_in_minutes} servings: {recipe.servings}>'

class RecipeDiet(db.Model):
    __tablename__ = 'recipe_diet'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)
    diet_id = db.Column(db.Integer, db.ForeignKey('diets.id', ondelete='cascade'), primary_key=True)

    def __repr__(self):
        recipe_diet = self
        return f'<Recipe Diet - recipe_id: {recipe_diet.recipe_id} diet_id: {recipe_diet.diet_id}>'

class RecipeCuisine(db.Model):
    __tablename__ = 'recipe_cuisine'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.id', ondelete='cascade'), primary_key=True)

    def __repr__(self):
        recipe_cuisine = self
        return f'<Recipe Cuisine - recipe_id: {recipe_cuisine.recipe_id} cuisine_id: {recipe_cuisine.cuisine_id}>'

class GroceryList(db.Model):
    __tablename__ = 'grocery_list'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)

    def __repr__(self):
        grocery_list = self
        return f'<Grocery List - user_id: {grocery_list.user_id} recipe_id: {grocery_list.recipe_id}>'

class Likes(db.Model):
    __tablename__ = 'likes'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)

    def __repr__(self):
        likes = self
        return f'<Likes - user_id: {likes.user_id} recipe_id: {likes.recipe_id}>'