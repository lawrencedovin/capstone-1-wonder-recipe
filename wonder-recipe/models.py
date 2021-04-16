from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, JSONB
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
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
                     nullable=False,
                     unique=True)
    email = db.Column(db.String(64),
                     nullable=False,
                     unique=True)
    password = db.Column(db.String(128),
                     nullable=False)
    phone_number = db.Column(db.String(16),
                     nullable=False)

    def __repr__(self):
        user = self
        return f'<User - id: {user.id} username: {user.username} email: {user.email} password: {user.password} phone_number: {user.phone_number}>'

    @classmethod
    def signup(cls, username, email, password, phone_number):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


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

    diets = db.relationship('Diet',
                            secondary='recipe_diet',
                            backref='recipe')

    cuisines = db.relationship('Cuisine',
                            secondary='recipe_cuisine',
                            backref='recipe')
    
    liked_by_users = db.relationship('User',
                            secondary='likes',
                            backref='liked_recipes')
    
    grocery_list_by_users = db.relationship('User',
                            secondary='grocery_list',
                            backref='grocery_list_recipes')

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