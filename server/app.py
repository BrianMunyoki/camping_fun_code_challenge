from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Welcome to the camping Trip</h1>'
#get all campers
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict(rules=('-signups', '-activities')) for camper in campers]), 200
#get each campers id
@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if camper:
       return jsonify(camper.to_dict()), 200
    return jsonify({"error": "Camper not found"}), 404
#posting each campers details
@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    try:
        camper = Camper(
            name=data.get('name'), 
            age=data.get('age')
        )
        db.session.add(camper)
        db.session.commit()
        return jsonify(camper.to_dict(rules=('-signups', '-activities'))), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
#Patching each capers details
@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    
    data = request.get_json()
    try:
        if 'name' in data:
            camper.name = data['name']
        if 'age' in data:
            camper.age = data['age']
        
        db.session.commit()
        return jsonify(camper.to_dict(rules=('-signups', '-activities'))), 202
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

#Quering all camping activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200
#Deleting each camping activity
@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    
    db.session.delete(activity)
    db.session.commit()
    return '', 204
#posting each sign up
@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    try:
        signup = Signup(
            time=data.get('time'),
            camper_id=data.get('camper_id'),
            activity_id=data.get('activity_id')
        )
        db.session.add(signup)
        db.session.commit()
        return jsonify(signup.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
