from app import app, db
from models import Camper, Activity, Signup

with app.app_context():
    db.drop_all()
    db.create_all()

    camper1=Camper(name="Brian",age=15)
    camper2=Camper(name="Jane",age=15)

    activity1=Activity(name="Hiking",difficulty="Medium")
    activity2=Activity(name="Swimming",difficulty="Easy")

    signup1=Signup(time=9, camper=camper1, activity=activity1)
    signup2=Signup(time=10, camper=camper1, activity=activity2)
    signup3=Signup(time=9, camper=camper2, activity=activity2)

    db.session.add_all([camper1,camper2,activity1,activity2,signup1,signup2,signup3])
    db.session.commit()
