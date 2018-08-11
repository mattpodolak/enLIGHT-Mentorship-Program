from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

flapp = Flask(__name__)
flapp.config.from_object(Config)
db = SQLAlchemy(flapp)
migrate = Migrate(flapp, db)
login = LoginManager(flapp)
login.login_view = 'login'

from app import routes, models