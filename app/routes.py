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

# route decorator
# @<flask object/bluprint name>.route('/url endpoint', <methods>)
# followed by a regular python function
@app.route('/')
def home():
    # this is a regular python function, I can write normal python code here
    greeting = 'Hello, Foxes!'
    print(greeting)
    # the return value of this function is what is displayed on the webpage
    return 'Hello, world.'