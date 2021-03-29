from flask_sqlalchemy import SQLAlchemy

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
    cuisine_name = db.Column(db.String(20),
                     nullable=False)

    def __repr__(self):
        cuisine = self
        return f'<Cuisine - id: {cuisine.id} cuisine_name: {cuisine.cuisine_name}>'