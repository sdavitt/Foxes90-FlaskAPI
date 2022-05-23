# our auth blueprint is designed to be a subsection with a specific role within our larger flask app
# we need to connect it to our larger flask app, otherwise we wont have access to it

# tools for blueprint and routing
from flask import Blueprint, render_template, request, redirect, url_for, flash

# define our blueprint/create the auth instance of a flask Blueprint/aka create the subsection of our application
auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth', static_folder='auth_static')

# import our Form(s)
from .authforms import LoginForm, RegistrationForm

# create our first route within the blueprint
# very similar to our main routes - the only difference is it will belong to the auth blueprint rather than the app
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # happens regardless of method -> we want access to the LoginForm on both GET and POST
    lform = LoginForm()
    # everything in this conditional only happens on POST request (aka form submission)
    if request.method == 'POST':
        if lform.validate_on_submit():
            # either the form data is proper and we want to log the user in
            # we'll need the username and the password from the form
            username = lform.username.data
            password = lform.password.data
            print('formdata:', username, password)
            # if they are successful in logging in, we want to send them to a different page and provide them with feedback that they are now signed in
            flash(f'Success - you have been signed in, {username}.', category='success')
            return redirect(url_for('home'))
        
        else:
            # or the form data is incorrect (bad username, bad password, etc.) - we don't want to sign the user in
            # we want to provide user feedback
            # and send them back to the signin page
            return redirect(url_for('auth.login'))
    # this return statement only applies to a GET request
    return render_template('signin.html', form=lform)


# a second auth route - registration
# accepts GET and POST requests
    # GET - shows the user our registration page (complete with form)
    # POST - the user has submitted the form
        # I want to check if their form submission is valid
        # Then check to make sure their registration information matches what I want (unique email? unique username? valid password?)
            # if everything checks out, register them, log them in, and redirect them to the home page
            # if there is a problem with registration, redirect them back to the registration page and provide feedback
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # utilize our form for both GET and POST
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # check db
            # access form data
            print(form.data) # all data as a dict
            print(form.email.data) # specifically the data of the email field
            flash('Welcome! Thank you for registering!', 'info')
            return redirect(url_for('home'))
        else: # something went wrong with registration
            flash('Sorry, passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    # GET -> create form instance, then rendering the hmtl template with that form
    elif request.method == 'GET':
        return render_template('register.html', form=form)