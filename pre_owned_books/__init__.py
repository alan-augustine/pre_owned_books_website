import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


#########################################################
# Initial APP SETUP #########################
#########################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'

#########################################################
# DATABASE SETUP ##########################
#########################################################
# before initial run of app.py below command from location of app.py
# activate virtualenv
# export FLASK_APP=app.py
# flask db init
# flask db migrate -m "initial setup"
# flask db upgrade

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#########################################################
# LOGIN SETUP ##########################
#########################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='core_blueprint.login'

#########################################################
# BLUE-PRINT SETUP ##########################
#########################################################

from pre_owned_books.core.views import core_blueprint
from pre_owned_books.users.views import users_blueprint

app.register_blueprint(core_blueprint)
app.register_blueprint(users_blueprint)
