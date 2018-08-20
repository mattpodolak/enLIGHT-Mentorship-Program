from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_bootstrap import Bootstrap

flapp = Flask(__name__)
flapp.config.from_object(Config)
db = SQLAlchemy(flapp)
migrate = Migrate(flapp, db)
login = LoginManager(flapp)
login.login_view = 'login'
bootstrap = Bootstrap(flapp)

# if not flapp.debug:
#     if flapp.config['MAIL_SERVER']:
#         auth = None
#         if flapp.config['MAIL_USERNAME'] or flapp.config['MAIL_PASSWORD']:
#             auth = (flapp.config['MAIL_USERNAME'], flapp.config['MAIL_PASSWORD'])
#         secure = None
#         if flapp.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(flapp.config['MAIL_SERVER'], flapp.config['MAIL_PORT']),
#             fromaddr='no-reply@' + flapp.config['MAIL_SERVER'],
#             toaddrs=flapp.config['ADMINS'], subject='enLIGHT Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         flapp.logger.addHandler(mail_handler)

from app import routes, models