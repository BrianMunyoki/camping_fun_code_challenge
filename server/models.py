from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()
class Camper(db.Model):
    __tablename__ = "campers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    @validates("name")
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("name must not be empty")
        return value

    @validates("age")
    def validate_age(self, key, value):
        if not isinstance(value, int):
            raise ValueError("age must be an integer")
        if value < 8 or value > 18:
            raise ValueError("age must be between 8 and 18")
        return value

    signups = db.relationship(
        "Signup",
        back_populates="camper",
        cascade="all, delete-orphan"
    )

    def to_dict(self, include_signups=False):
        data = {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }

        if include_signups:
            data["signups"] = [
                {
                    "id": s.id,
                    "time": s.time,
                    "activity": {
                        "id": s.activity.id,
                        "name": s.activity.name
                    }
                }
                for s in self.signups
            ]

        return data

    def __repr__(self):
        return f"<Camper {self.name}>"


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.String)

    signups = db.relationship(
        "Signup",
        back_populates="activity",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "difficulty": self.difficulty
        }

    def __repr__(self):
        return f"<Activity {self.name}>"


class Signup(db.Model):
    __tablename__ = "signups"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)

    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))

    @validates("time")
    def validate_time(self, key, value):
        if not isinstance(value, int):
            raise ValueError("time must be an integer")
        if value < 0 or value > 23:
            raise ValueError("time must be between 0 and 23")
        return value

    camper = db.relationship("Camper", back_populates="signups")
    activity = db.relationship("Activity", back_populates="signups")

    def to_dict(self, include_nested=False):
        data = {
            "id": self.id,
            "time": self.time
        }

        if include_nested:
            data["camper"] = self.camper.to_dict()
            data["activity"] = self.activity.to_dict()

        return data

    def __repr__(self):
        return f"<Signup Camper={self.camper_id} Activity={self.activity_id}>"
