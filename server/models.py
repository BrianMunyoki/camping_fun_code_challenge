from flask_sqlalchemy import SQLAlchemy
from app import db

class Camper(db.Model):
    __tablename__='campers'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    age=db.Column(db.Integer)

    #relationships
    signups=db.relationships('Signup',back_populates='Camper',cascade='all, delete-orphan')

    def __repr__(self):
        return f'<camper{self.name}'

class Activity(db.Model):
     __tablename__='activities'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.string)
    difficulty=db.Column(db.string)
    #relationships
    signups=db.relationships('signup', back_populates='Activity',cascade='all, delete orphan')

    def __repr__(self):
        return f'<Activity {self.name}>'
class Signup(db.Model):
     __tablename__='signups'
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.Integer)

    camper_id=db.Column(db.Integer, db.ForeignKey('Campers.id'))
    activity_id=db.Column(db.Iteger, db.ForeignKey('activities.id'))
    #relationships
    camper=db.relationship('Camper',back_populates='Signups')
    activity=db.relationship('Activity', back_populates='signups')

    def __repr__(self):
        return f'<Signup Camper={self.camper_id} Activity={self.activity_id}'
