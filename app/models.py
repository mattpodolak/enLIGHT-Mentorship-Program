from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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
    #in db.relat... referenced by model class ie: Post
    #posts is not a db field, defined one the "one" side of one-to-many relation
    #backref defines name of field for the "many" objs
    #lazy defines database query for relationship
    users = db.relationship('User', backref='mentor', lazy='dynamic')

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

    def __repr__(self):
        return '<Mentor {}>'.format(self.email)

class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64))
    users = db.relationship('User', backref='type', lazy='dynamic')


    def __repr__(self):
        return '<Type {}>'.format(self.account)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #in db.Fore... reference user.id user is database table name, referencing the id from this table
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)