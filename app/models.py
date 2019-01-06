from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib
from time import time
import jwt
from app import flapp


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    about_me = db.Column(db.String(280))
    avail = db.Column(db.String(64))
    skill = db.Column(db.String(164))
    industry = db.Column(db.String(164))
    company = db.Column(db.String(164))
    position = db.Column(db.String(164))
    linked = db.Column(db.String(164))
    # twitter = db.Column(db.String(164))
    #in db.relat... referenced by model class ie: Post
    #posts is not a db field, defined one the "one" side of one-to-many relation
    #backref defines name of field for the "many" objs
    #lazy defines database query for relationship
    users = db.relationship('User', backref='mentor', lazy='dynamic')
    mentee_pref_id = db.Column(db.Integer, db.ForeignKey('mentee.id'))
    cohort_pref_id = db.Column(db.Integer, db.ForeignKey('cohort.id'))

    def __repr__(self):
        return '<Mentor {}>'.format(self.email)

class Mentee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    founder = db.Column(db.String(280))
    email = db.Column(db.String(120), index=True, unique=True)
    industry = db.Column(db.String(280))
    skills = db.Column(db.String(280))
    help_req = db.Column(db.String(280))
    mentor1 = db.Column(db.String(128))
    mentor2 = db.Column(db.String(128))
    mentor3 = db.Column(db.String(128))

    prefs = db.relationship('Mentor', backref='mentee', lazy='dynamic')

    def __repr__(self):
        return '<Mentee {}>'.format(self.email)

class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    founder = db.Column(db.String(280))
    email = db.Column(db.String(120), index=True, unique=True)
    industry = db.Column(db.String(280))
    skills = db.Column(db.String(280))
    help_req = db.Column(db.String(280))
    mentor1 = db.Column(db.String(128))
    mentor2 = db.Column(db.String(128))
    mentor3 = db.Column(db.String(128))

    prefs = db.relationship('Mentor', backref='cohort', lazy='dynamic')

    def __repr__(self):
        return '<Cohort {}>'.format(self.email)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accept = db.Column(db.String(100))
    company = db.Column(db.String(100))
    founder = db.Column(db.String(280))
    email = db.Column(db.String(120), index=True, unique=True)
    industry = db.Column(db.String(280))
    skills = db.Column(db.String(280))
    help_req = db.Column(db.String(280))
    interest = db.Column(db.String(500))
    gain = db.Column(db.String(500))
    stage = db.Column(db.String(100))
    relation = db.Column(db.String(280))
    web = db.Column(db.String(280))
    links = db.Column(db.String(380))

    def __repr__(self):
        return '<Application {}>'.format(self.email)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email_hash = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer)
    #in db.Fore... reference user.id user is database table name, referencing the id from this table
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))

    def is_admin(self):
        if(self.access == 2):
            return True
        return False
    
    def is_mentor(self):
        if(self.access == 1):
            return True
        return False

    def is_cohort(self):
        if(self.access == 3):
            return True
        return False

    def set_id(self):
        encode_string = self.email + str(self.id)
        hash_object = hashlib.md5(encode_string.encode())
        self.email_hash = hash_object.hexdigest()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            flapp.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, flapp.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.email)