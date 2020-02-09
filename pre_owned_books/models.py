from pre_owned_books import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# If we don't specify this function, we will get below error:
# Exception: No user_loader has been installed for this LoginManager.
# Refer to https://flask-login.readthedocs.io/en/latest/#how-it-works for more info.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    #TODO: return None (not raise an exception) if the ID is not valid

# This class represents a table to store User data
# We interact with the DB(Sqlite) through db object(imported above) and objects of 'User' class
# UserMixin - provides default implementations for the methods that Flask-Login expects user objects to have
# https://flask-login.readthedocs.io/en/latest/#user-object-helpers
class User(db.Model, UserMixin):

    #__tablename__ = 'users'

    # id is auto-generated
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password_plain_text):
        self.username = username
        self.password_hash = generate_password_hash(password_plain_text)

    def check_password(self, password_text):
        return check_password_hash(self.password_hash, password_text)

    def __repr__(self):
        return "This is DB entry for user: " + self.username