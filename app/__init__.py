from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flapp = Flask(__name__)
flapp.config.from_object(Config)
db = SQLAlchemy(flapp)
migrate = Migrate(flapp, db)

from app import routes, models