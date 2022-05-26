# the purpose of this file is simply to give my terminal and flask shell access to components of my app
# so that I can test them through the shell/CLI and not worry about templating or routing

# when you want to do testing through the flask shell with this context processor
# change the FLASK_APP variable in .env to run.py

# import the things we need
from app import app
from app.models import db, Animal, User, Post

# creating the shell context processor
@app.shell_context_processor
def shell_context():
    return {'db': db, 'Animal': Animal, 'User': User, 'Post': Post}