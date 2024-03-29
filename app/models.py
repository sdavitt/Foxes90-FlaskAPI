# This file is responsible for everything database
# Primarily the instantiation of our ORM and the creation of our database tables (models/entities)

# import our orm
from flask_sqlalchemy import SQLAlchemy
# create the instance of our ORM (object relational mapper)
db = SQLAlchemy()

# setup login manager
from flask_login import LoginManager, UserMixin
# create the instance of our LoginManager
login = LoginManager()

# tell our login manager how it can access a User object from a user_id
@login.user_loader
def load_user(userid):
    return User.query.get(userid)

# tools for our models
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash

# create a DB model -> aka a Python object that will be a table/entity in our SQL database
# create our User model
class User(db.Model, UserMixin):
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), default='No bio.')
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    api_token = db.Column(db.String(100))
    posts = db.relationship('Post', backref='post_author') # tells the User model that it has a relationship with the Post model

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = str(uuid4())
        self.password = generate_password_hash(password)

# Post model - one User can have many Posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    author = db.Column(db.String, db.ForeignKey('user.id')) # create a foreign key to another db.Model

# Animal model overhaul for api
class Animal(db.Model):
    # global attributes for each column in the database
    id = db.Column(db.String(40), primary_key=True)
    species = db.Column(db.String(50), nullable=False, unique=True)
    latin_name = db.Column(db.String(255))
    size_cm = db.Column(db.Integer)
    diet = db.Column(db.String(255))
    lifespan = db.Column(db.String(255))
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    price = db.Column(db.Float(2), nullable=False) # the number specified in the Float is the number of decimal places
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    # when a user submits a POST request to CREATE a new Animal, we want to use this __init__ method to handle the animal creation
    def __init__(self, dict):
        # some of these values are required
        self.id = str(uuid4())
        self.species = dict['species'].title()
        self.description = dict['description']
        self.price = dict['price']
        # some are optional
        self.image = dict.get('image') # if no image key, value will be None
        self.size_cm = dict.get('size_cm', 0) # if no size key, value will be 0
        self.latin_name = dict.get('latin_name', 'unknown')[0].upper() + dict.get('latin_name', 'unknown')[1:].lower() # if no image key, value will be 'Unknown'
        self.diet = dict.get('diet', 'unknown')
        self.lifespan = dict.get('lifespan', 0)


    # write a function to translate this object to a dictionary for jsonification
    # the other advantage to writing this function is that we can purposely not include some attributes if we don't want them
    def to_dict(self):
        return {
            'id': self.id,
            'species': self.species,
            'latin_name': self.latin_name,
            'image': self.image,
            'description': self.description,
            'price': self.price,
            'size_cm': self.size_cm,
            'diet': self.diet,
            'lifespan': self.lifespan,
            'created_on': self.created_on
        }

    # accepts a dictionary containing attributes that should be changed
    # then goes and changes whichevery attributes are present in the dictionary
    def from_dict(self, dict):
        # for each key that is in the dictionary, I want to redefine the associated variable
        for key in dict:
            getattr(self, key) # try to get the attribute such that we error if a non-existent attribute was provided
            setattr(self, key, dict[key]) # same as self.attribute = value
