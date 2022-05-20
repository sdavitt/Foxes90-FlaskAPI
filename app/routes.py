# flask routes control what content is shown on what url
    # depending on how the user is accessing the url (methods), what buttons they've pressed, or what requests they've made, what their permissions are, etc.

# the general structure of a flask route is a function with a decorator
# the decorator adds another function/lines of code that run before and/or after the function being decorated

# our first route:
# just display 'hello world' on our localhost url (when we run a flask app locally, it will default run on the following url)
    # http://127.0.0.1:5000/

# in order to set up a route we need a few tools
# 1. we need access to our Flask object
from app import app
# 2. we need to be able to return an html file from our flask routes
# using render_template() from the flask package
from flask import render_template


# import other packages we need
import requests as r
from .services import getF1Drivers

# route decorator
# @<flask object/bluprint name>.route('/url endpoint', <methods>)
# followed by a regular python function
@app.route('/')
def home():
    # this is a regular python function, I can write normal python code here
    greeting = 'Welcome to flask week, Foxes!'
    print(greeting)
    students = ['Jose', 'Kristen', 'Tyler', 'Craig', 'Yasir', 'Sven', 'Enrique', 'BT', 'DeVante', 'Nadia', 'Donovan']
    # the return value of this function is what is displayed on the webpage
    return render_template('index.html', greeting=greeting, students=students)


@app.route('/about')
def about():
    return render_template('about.html')


# let's look at a more complex example of routing and using python code
@app.route('/drivers')
def f1Drivers():
    # make an API call and utilize information from that API call in the HTML templating
    # in order to make an API call we need the requests package... let's install and import the requests package
    context = getF1Drivers() # sets the value of the context variable to a dictionary - the return value of the getF1Drivers function
    return render_template('f1.html', **context)


