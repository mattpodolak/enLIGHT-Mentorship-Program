from app import flapp, db
from app.models import User, Post

#flask shell invokes this function, registering included items
@flapp.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}