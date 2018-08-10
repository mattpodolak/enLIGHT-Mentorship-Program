from datetime import datetime
from app import db

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #in db.relat... referenced by model class ie: Post
    #posts is not a db field, defined one the "one" side of one-to-many relation
    #backref defines name of field for the "many" objs
    #lazy defines database query for relationship
    users = db.relationship('User', backref='mentor', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #in db.Fore... reference user.id user is database table name, referencing the id from this table
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)