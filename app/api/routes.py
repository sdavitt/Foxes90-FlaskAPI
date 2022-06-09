# initial blueprint setup
from flask import Blueprint, jsonify, request
import stripe
import os

api = Blueprint('api', __name__, url_prefix='/api')

# imports for api routes
from app.models import Animal, db
from .services import token_required

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
    # read a single animal's data based on their name [GET]
    # create a new animal [POST]
    # modify an existing animal's attributes [POST]
    # delete an animal [DELETE]
# 3. Protecting our API (auth system)

@api.route('/animals', methods=['GET'])
def getAnimals():
    """
    [GET] Retrieves all animal objects from our database and returns them as JSON data
    """
    # here, we won't get any additional information with the API request, we're just trying to query all animals from the database and then return them as JSON data
    # we can get all animals from the database with a single query returning a list of animal objects
    animals = Animal.query.all()
    # we discovered that we cannot directly JSONify a Python object
    # so we need to transform this list of animals into either a list of dictionaries or a dictionary of dictionaries or some similar structure
    print(animals)
    #animals = [a.to_dict() for a in animals] # list comprehension version
    animals = {a.id: a.to_dict() for a in animals} # dictionary comprehension version
    return jsonify(animals), 200

@api.route('/animal/<string:name>', methods=['GET'])
def getAnimalName(name):
    """
    [GET] retrieving a single animal from the database based on that animal's name
    """
    # get an animal name in from the dynamic route URL
    print(name)
    # query the database for that animal
    animal = Animal.query.filter_by(species=name.title()).first()
    # if it exists, return the animal as a JSONified dicitonary
    if animal:
        return jsonify(animal.to_dict()), 200
    # otherwise return an error message
    return jsonify({'error': f'no such animal with the name: {name.title()}'}), 404


@api.route('/create', methods=['POST'])
@token_required
def createAnimal():
    '''
    [POST] create a new animal in our database with data provided in the request body
    expected data format: JSON:
        {
            'species': <str>,
            'description': <str>,
            'price': <numeric>,
            # all other K:V pairs optional
            'latin_name': <str>,
            'image': <str>,
            'size_cm': <int>,
            'diet': <str>,
            'lifespan':<str>
        }
    '''
    try:
        # we want the user to pass in a dictionary in the body of the request
        # we will access that dictionary
        newdict = request.get_json()
        print(newdict)
        # and use it to instantiate an instance of an Animal object
        a = Animal(newdict)
        print(a)
    except:
        return jsonify({'error': 'improper request or body data'}), 400
    try:
        # then save that animal object to our database
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error': 'species already exists in the database'}), 400
    # and tell our user that the operation was successful
    return jsonify({'created': a.to_dict()}), 200

@api.route('/update/<string:id>', methods=['POST'])
@token_required
def updateAnimal(id):
    '''
    [POST] updates an existing animal in our database with data provided in the request body
    expected data format: JSON:
        {
            # ALL K:V pairs optional, must have at least one
            'species': <str>,
            'description': <str>,
            'price': <numeric>,
            'latin_name': <str>,
            'image': <str>,
            'size_cm': <int>,
            'diet': <str>,
            'lifespan':<str>
        }
    '''
    try:
        # access the request body
        newvals = request.get_json()
        # query our database for an animal with the provided id
        animal = Animal.query.get(id)
        # update that animal's attributes using the provided dictionary and our from_dict function
        animal.from_dict(newvals)
        # save those updates in our database
        db.session.commit()
        return jsonify({'Updated animal': animal.to_dict()}), 200
    except:
        return jsonify({'Request failed': 'Invalid request or animal ID does not exist.'}), 400
    
@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def removeAnimal(id):
    """
    [DELETE] accepts an animal ID - if that ID exists in the database, remove that animal and return the removed animal object
    """
    # check if the animal exists
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'Remove failed': f'No animal with ID {id} in the database.'}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'Removed animal': animal.to_dict()}), 200


# stripe section - payment assurance calculations and payment intent creation

# set our api_key
stripe.api_key = os.environ.get('STRIPE_SECRET')

# functions to help create payment intent:
def checkTotal(cart):
    """
    return the proper payment amount for this cart
    """
    # total = 0
    # # this for loop calculates the cart total based on the prices in our database (that the client has no chance of manipulating)
    # for animal in cart['items']:
    #     price = Animal.query.get(cart['items'][animal]['obj']['id']).price
    #     total += price
    # print('calculated total from DB')
    # # after the loop, total is what the cart total should be based on prices in my database
    # # cart['total'] would be the cart's total according to the frontend/react app
    # # return the total if the totals match and are what I'm expecting, otherwise return None because the payment amount for this payment is incorrect
    # # and we dont want it to go through (returning none will cause an error in the PaymentIntent creation)
    # # return int(total*100) if round(total, 2) == round(cart['total'], 2) else None
    
    # alternative return statement because I'm using an older API for my react app
    return int(cart['total']*100)

def getCustomer(u):
    """
    check stripe for an existing customer with this id
    if one exists, return that stripe Customer object
    otherwise create a new Customer object with this information
    """
    print('getting customer')
    try:
        return stripe.Customer.retrieve(u['uid'])
    except:
        return stripe.Customer.create(id=u['uid'], name=u['displayName'], email=u['email'])


# set up the create payment intent route
@api.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = request.get_json() # {'cart': <cart>, 'user': <user>}
        # Create a PaymentIntent with the order amount and currency
        print('check')
        intent = stripe.PaymentIntent.create(
            amount=checkTotal(data['cart']),
            currency='eur',
            payment_method_types=['card'],
            customer=getCustomer(data['user'])
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 403