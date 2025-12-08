from flask_sqlalchemy import SQLAlchemy
from app import db


class Camper(db.Model):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    @validates('name')
    def validate_name(self,key,value):
        if value=="":
            raise ValueError("value must not be empty")
        return value
    @validate("age")
    def validate_age(self,key,value):
        if not isinstance(Value,int):
            raise ValueError("value must be an integer")
        if Value ,8 or Value> 18:
            raise ValueError("age must be between 8 and 18")
        return Value
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

    @validates("time")
    def validate_time(key,value):
        if no isinstance(value,int):
            raise ValueError("time must be an integer")
        if value <0 or value>24:
            raise ValueError("time must be between 0 and 24")
        return value

    # Relationship
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    def __repr__(self):
        return f'<Signup Camper={self.camper_id} Activity={self.activity_id}>'
