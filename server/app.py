from flask import Flask
from flask_sqlalchemy import flask_sqlalchemy
from flask_migrate import Migrate 

app=Flask(__name__)
#create app
@app.route('/')

#data base configuration

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///camp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize extensions

db=SQLAlchemy(app)
migrate=Migrate(app,db)


def home():
    return "API is running!"

if __name__=="__main__":
    app.run(port=5555,debug=True)