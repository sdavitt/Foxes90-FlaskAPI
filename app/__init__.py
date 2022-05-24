# the backbone of the flask app
# all other pieces of the flask app must connect back to this file
# and this file is the hub of all communication between independent pieces of the flask app

# from the flask package import the Flask object/class
from flask import Flask
# from the config file import the Config class that we created
from config import Config

# import blueprints for registration
from .auth.routes import auth

# imports for database stuff
from .models import db
from flask_migrate import Migrate


# define/instantiate our Flask app... aka create the actual object that will be our Flask app
app = Flask(__name__)

# tell this app how it is going to be configured
app.config.from_object(Config)
# aka configuring our flask app based on the Config class we made in the config.py file

# create the link of communication between blueprints and app
# aka register our blueprints
app.register_blueprint(auth)

# set up ORM and Migrate communication with app and eachother
db.init_app(app) # if this isnt here, our app and our database don't know how to talk to eachother (for queries, adding data, etc.)
migrate = Migrate(app, db) # this is actually giving us the ability to modify database structure from our flask app (aka create tables, etc.)


# our flask app is really dumb. if we do not tell it about the existence of other files, it will assume they do not exist
# import the routes file here so that our Flask app knows the routes exist
# this is one of the only scenarios where imports will be at the bottom of a file 
    # these imports MUST be after the instantiation of the flask app (line 11) and the configuration (line 14)
from . import routes # from the app folder (this folder), import the entire routes file