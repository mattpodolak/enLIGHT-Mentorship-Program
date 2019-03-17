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
    headline = db.Column(db.String(100))
    about_me = db.Column(db.String(280))
    avail = db.Column(db.String(64))
    skills = db.Column(db.String(164))
    industry = db.Column(db.String(164))
    mentor_company = db.Column(db.String(164))
    position = db.Column(db.String(164))
    university = db.Column(db.String(280))
    major = db.Column(db.String(280))
    grad_year = db.Column(db.String(128))
    linkedin = db.Column(db.String(164))
    twitter = db.Column(db.String(164))
    #in db.relat... referenced by model class ie: Post
    #posts is not a db field, defined one the "one" side of one-to-many relation
    #backref defines name of field for the "many" objs
    #lazy defines database query for relationship

    #connects to user to assign a mentor to an acct
    users = db.relationship('User', backref='mentor', lazy='dynamic')

    #these track mentor preferences for mentee and cohort users
    mentee_pref_id = db.Column(db.Integer, db.ForeignKey('mentee.id'))
    company_pref_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Mentor {}>'.format(self.email)

class Mentee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    headline = db.Column(db.String(100))
    about = db.Column(db.String(280))
    company = db.Column(db.String(100))
    university = db.Column(db.String(280))
    major = db.Column(db.String(280))
    year = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    industry = db.Column(db.String(280))
    skills = db.Column(db.String(280))
    mentor1 = db.Column(db.String(128))
    mentor2 = db.Column(db.String(128))
    mentor3 = db.Column(db.String(128))
    linkedin = db.Column(db.String(164))
    twitter = db.Column(db.String(164))

    #connects to mentor to track the mentor prefs of mentee
    prefs = db.relationship('Mentor', backref='mentee', lazy='dynamic')

    #connects to user to help track mentee prefs for mentors
    mentor_pref_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #tracks what company they work for
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Mentee {}>'.format(self.email)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    about = db.Column(db.String(280))
    members = db.Column(db.String(280))
    email = db.Column(db.String(340))
    industry = db.Column(db.String(280))
    help_req = db.Column(db.String(280))
    mentor1 = db.Column(db.String(128))
    mentor2 = db.Column(db.String(128))
    mentor3 = db.Column(db.String(128))

    #connects to mentor to track the mentor prefs of cohort
    prefs = db.relationship('Mentor', backref='company', lazy='dynamic')

    #connects to mentee to track the mentor prefs of cohort
    members_l = db.relationship('Mentee', backref='company_l', lazy='dynamic')

    #connects to user to help track mentee prefs for mentors
    mentor_pref_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Company {}>'.format(self.email)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accept = db.Column(db.String(100))
    company = db.Column(db.String(100))
    founder = db.Column(db.String(280))
    email = db.Column(db.String(340))
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
    profile_pic = db.Column(db.String(188))
    access = db.Column(db.Integer)
    #in db.Fore... reference user.id user is database table name, referencing the id from this table
    #connects to mentor so a mentor can be assigned to an acct
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))

    #tracks mentee preferences for mentor accts
    prefs_m = db.relationship('Mentee', backref='mentorpref', lazy='dynamic')
    prefs_c = db.relationship('Company', backref='mentorpref', lazy='dynamic')

    def is_admin(self):
        if(self.access == 2):
            return True
        return False
    
    def is_mentor(self):
        if(self.access == 1):
            return True
        return False

    def is_company(self):
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