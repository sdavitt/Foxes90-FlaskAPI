# the backbone of the flask app
# all other pieces of the flask app must connect back to this file
# and this file is the hub of all communication between independent pieces of the flask app

# from the flask package import the Flask object/class
from flask import Flask
# from the config file import the Config class that we created
from config import Config

# define/instantiate our Flask app... aka create the actual object that will be our Flask app
app = Flask(__name__)

# tell this app how it is going to be configured
app.config.from_object(Config)
# aka configuring our flask app based on the Config class we made in the config.py file

# our flask app is really dumb. if we do not tell it about the existence of other files, it will assume they do not exist
# import the routes file here so that our Flask app knows the routes exist
# this is one of the only scenarios where imports will be at the bottom of a file 
    # these imports MUST be after the instantiation of the flask app (line 11) and the configuration (line 14)
from . import routes # from the app folder (this folder), import the entire routes file