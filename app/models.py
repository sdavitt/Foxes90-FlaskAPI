# This file is responsible for everything database
# Primarily the instantiation of our ORM and the creation of our database tables (models/entities)

# import our orm
from flask_sqlalchemy import SQLAlchemy
# create the instance of our ORM (object relational mapper)
db = SQLAlchemy()

# tools for our models
from datetime import datetime

# create a DB model -> aka a Python object that will be a table/entity in our SQL database
class Animal(db.Model):
    # global attributes for each column in the database
    id = db.Column(db.Integer, primary_key=True) # we need to provide at least a datatype (we can also provide default values and/or constraints)
    name = db.Column(db.String(50), nullable=False)
    latin = db.Column(db.String(255), default=None)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    cool = db.Column(db.Boolean, default=True) # i think