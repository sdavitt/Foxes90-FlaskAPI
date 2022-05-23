# our auth blueprint is designed to be a subsection with a specific role within our larger flask app
# we need to connect it to our larger flask app, otherwise we wont have access to it

# tools for blueprint and routing
from flask import Blueprint, render_template, request

# define our blueprint/create the auth instance of a flask Blueprint/aka create the subsection of our application
auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth', static_folder='auth_static')

# import our Form(s)
from .authforms import LoginForm

# create our first route within the blueprint
# very similar to our main routes - the only difference is it will belong to the auth blueprint rather than the app
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # happens regardless of method -> we want access to the LoginForm on both GET and POST
    lform = LoginForm()
    # everything in this conditional only happens on POST request (aka form submission)
    if request.method == 'POST':
        print(lform.data)
        return 'Thanks for logging in.' # prevents any code after this from running
    
    # this return statement only applies to a GET request
    return render_template('signin.html', form=lform)