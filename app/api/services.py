# We're going to be building a token_required decorator
# Essentially, this will perform the same role for API routes that the login_required decorator performs for templated routes

# General structure of a custom decorator:
# A closure -> defining a function inside of another function where the inner function is returned by the outer function

# outer function with the name of the custom decorator
    # @wraps()
    # inner function
        # code to run before the decorated function runs
        # can either return the decorated function (causing it to run like normal)
        # or return something else, preventing the decorated function from running
    # return the inner function
from flask import request, jsonify
from functools import wraps
from app.models import User

def token_required(api_route):
    @wraps(api_route)
    def decorator_function(*args, **kwargs):
        # code here will run before the decorated function (the api route) runs
        # try to get the access token
        token = request.headers.get('foxes-access-token')
        # if there is no token - stop the request and send a forbidden message
        if not token:
            return jsonify({'Access denied': 'No API token - please register to receive your API token.'}), 401
        # if there is a token - check if it a valid token, if not valid, stop the request and send a forbidden message
        if not User.query.filter_by(api_token=token).first():
            return jsonify({'Invalid API token': 'Please check your API token or request a new one.'}), 403
        # if the token is present and valid, allow the request to go through
        return api_route(*args, **kwargs)
    return decorator_function