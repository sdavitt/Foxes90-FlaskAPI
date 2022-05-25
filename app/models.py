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
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, username, email, password, first_name='', last_name=''):
        self.username = username
        self.email = email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = str(uuid4())
        self.password = generate_password_hash(password)

# Animal model overhaul for api
class Animal(db.Model):
    # global attributes for each column in the database
    id = db.Column(db.String(40), primary_key=True)
    species = db.Column(db.String(50), nullable=False)
    latin_name = db.Column(db.String(255))
    size_cm = db.Column(db.Integer)
    diet = db.Column(db.String(255))
    lifespan = db.Column(db.String(255))
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(100))
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


    
