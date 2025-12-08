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


if __name__=="__main__":
    app.run(port=5555,debug=True)