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

    