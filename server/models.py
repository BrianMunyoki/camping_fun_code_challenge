from flask_sqlalchemy import SQLAlchemy
from app import db


class Camper(db.Model):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Relationship
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Camper {self.name}>'


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.String)

    # Relationship
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Activity {self.name}>'


class Signup(db.Model):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    # Relationship
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    def __repr__(self):
        return f'<Signup Camper={self.camper_id} Activity={self.activity_id}>'
