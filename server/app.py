from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app=Flask(__name__)
#create app


#data base configuration

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///camp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize extensions

db=SQLAlchemy(app)
migrate=Migrate(app,db)



@app.get("/campers")
def get_campers():
    campers = Camper.query.all()
    return jsonify([c.to_dict() for c in campers]), 200

@app.get("/campers/<int:id>")
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify(camper.to_dict(include_signups=True)), 200
@app.post("/campers")
def create_camper():
    data = request.get_json()

    try:
        camper = Camper(name=data.get("name"), age=data.get("age"))
        db.session.add(camper)
        db.session.commit()
        return camper.to_dict(), 201

    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
@app.patch("/campers/<int:id>")
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.get_json()

    try:
        if "name" in data:
            camper.name = data["name"]
        if "age" in data:
            camper.age = data["age"]

        db.session.commit()
        return camper.to_dict(), 202

    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
@app.get("/activities")
def get_activities():
    activities = Activity.query.all()
    return jsonify([a.to_dict() for a in activities]), 200
@app.delete("/activities/<int:id>")
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()
    return "", 204
@app.post("/signups")
def create_signup():
    data = request.get_json()

    try:
        signup = Signup(
            time=data.get("time"),
            camper_id=data.get("camper_id"),
            activity_id=data.get("activity_id")
        )

        db.session.add(signup)
        db.session.commit()

        return signup.to_dict(include_nested=True), 201

    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400
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
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "difficulty": self.difficulty
    }
def to_dict(self, include_nested=False):
    data = {
        "id": self.id,
        "time": self.time
    }

    if include_nested:
        data["camper"] = self.camper.to_dict()
        data["activity"] = self.activity.to_dict()

    return data


if __name__=="__main__":
    app.run(port=5555,debug=True)