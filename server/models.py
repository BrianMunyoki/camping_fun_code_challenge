from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()


# CAMPERS TABLE

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Relationship bentween sign up an campers
    signups = db.relationship(
        'Signup',
        back_populates='camper',
        cascade='all, delete-orphan',
        overlaps="activities,campers"
    )

    # Realtionship between activity and sign ups
    activities = db.relationship(
        'Activity',
        secondary='signups',
        back_populates='campers',
        overlaps="signups,activity"
    )

    # Prevent recursion across all relationship paths
    serialize_rules = (
        '-signups.camper',
        '-signups.activity',
        '-activities.campers',
        '-activities.signups'
    )

    # name validations
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required")
        return name

    # age validation
    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age < 8 or age > 18:
            raise ValueError("Age must be between 8 and 18")
        return age

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'

#              ACTIVITIES TABLE

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    # relationshi between sign up and activvity
    signups = db.relationship(
        'Signup',
        back_populates='activity',
        cascade='all, delete-orphan',
        overlaps="campers,activities"
    )

    # relationship between camper and sign up
    campers = db.relationship(
        'Camper',
        secondary='signups',
        back_populates='activities',
        overlaps="signups,camper"
    )

    # Prevent all recursion paths: signups, campers, and their reverse loops
    serialize_rules = (
        '-signups.activity',
        '-signups.camper',
        '-campers.activities',
        '-campers.signups'
    )

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'
# SIGNUPS TABLE

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    # relationship between camper and signup
    camper = db.relationship(
        'Camper',
        back_populates='signups',
        overlaps="activities,campers"
    )

    # relationship between activity and relationshp
    activity = db.relationship(
        'Activity',
        back_populates='signups',
        overlaps="activities,campers"
    )

    # Prevent recursion when serializing signups
    serialize_rules = (
        '-camper.signups',
        '-camper.activities',
        '-activity.signups',
        '-activity.campers'
    )

    # time validator
    @validates('time')
    def validate_time(self, key, time):
        if not isinstance(time, int) or time < 0 or time > 24:
            raise ValueError("Time must be between 0 and 24")
        return time

    def __repr__(self):
        return f'<Signup {self.id}: Camper {self.camper_id} -> Activity {self.activity_id}>'
