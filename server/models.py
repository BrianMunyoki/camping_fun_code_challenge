from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    signups = db.relationship('Signup', back_populates='camper', cascade='all, delete-orphan')
    activities = db.relationship('Activity', secondary='signups', back_populates='campers')
    
    serialize_rules = ('-signups.camper', '-activities.campers')
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name
    
    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age < 8 or age > 18:
            raise ValueError("Age must be between 8 and 18")
        return age
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    
    signups = db.relationship('Signup', back_populates='activity', cascade='all, delete-orphan')
    campers = db.relationship('Camper', secondary='signups', back_populates='activities')
    
    serialize_rules = ('-signups.activity', '-campers.activities')
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
    
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    
    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')
    
    serialize_rules = ('-camper.signups', '-activity.signups')
    
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 24:
            raise ValueError("Time must be between 0 and 24")
        return time
    
    def __repr__(self):
        return f'<Signup {self.id}: Camper {self.camper_id} -> Activity {self.activity_id}>'
