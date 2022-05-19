# set up and organizing the application file structure and configuration
# what secret variables does the app need
# and where is the base directory/root folder of the project

# we're gonna need a little help from the os package
import os

# set up the base directory of the entire application - aka help our computer understand this app's file structure
basedir = os.path.abspath(os.path.dirname(__name__))

# set up a class for our configuration variables
class Config:
    """
    setting configuration variables that tell our flask app how to run
    """
    # all three of these values should not be public information - we should keep these values hidden
        # their actual value will exist in the .env file
        # their value here will just be a function call to access that value in the .env file
    FLASK_APP = os.environ.get('FLASK_APP') # go get the FLASK_APP variable value from the .env file
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')