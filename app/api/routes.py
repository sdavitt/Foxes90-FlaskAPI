# initial blueprint setup
from flask import Blueprint, jsonify

api = Blueprint('api', __name__, url_prefix='/api')

# imports for api routes
from app.models import Animal

# an API endpoint is just a regular route that returns JSON data instead of a render template or redirect

# initial testing route
@api.route('/test', methods=['GET'])
def test():
    # jsonify? transforms python data into json data
    # we can return a status code alongside this
    # query database for an Animal
    fox = Animal.query.all()[0]
    # JSONify a dictionary version of that animal object and return that jsonified data to the endpoint
    return jsonify(fox.to_dict()), 200

# The purpose of this API is going to be to hold a database of products that we will use on our mock ecommerce store that we will create in React
# We are making a CRUD API that create, read, update, and/or delete Animals from our database
# so, what attributes/columns/information do we need for each Animal
    # what can be changed? what shouldn't be changed? what is required?

# 1. Set up our Animal model so that it can hold all the data we need
# 2. Set up routing here in our API so that an API request can: 
    # read all animal data [GET]
    # read a single animal's data based on their ID or maybe name [GET]
    # create a new animal [POST]
    # modify an existing animal's attributes [POST]
    # delete an animal [DELETE]
# 3. Protecting our API (auth system)