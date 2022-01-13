from flask_sqlalchemy import SQLAlchemy
from service import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./predictions.db'
db = SQLAlchemy(app)


def insert_prediction(input_attributes, prediction, model_name):
    prediction_record = input_attributes
    prediction_record['prediction'] = prediction
    prediction_record['model'] = model_name

    db.session.add(Prediction(prediction_record))
    db.session.commit()


class Prediction(db.Model):
    def __init__(self, prediction_dict):
        self.model = prediction_dict['model']
        self.user_id = prediction_dict['user_id']
        self.duration = prediction_dict['duration']
        self.price = prediction_dict['price']
        self.click_rate = prediction_dict['click_rate']
        self.last_session_purchase = prediction_dict['last_session_purchase']
        self.weekday = prediction_dict['weekday']
        self.hour = prediction_dict['hour']
        self.offered_discount = prediction_dict['offered_discount']
        self.weekend = prediction_dict['weekend']
        self.prediction = prediction_dict['prediction']

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    click_rate = db.Column(db.Float, nullable=False)
    last_session_purchase = db.Column(db.Boolean, nullable=False)
    weekday = db.Column(db.Integer, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    offered_discount = db.Column(db.Integer, nullable=False)
    weekend = db.Column(db.Boolean, nullable=False)
    prediction = db.Column(db.Boolean, nullable=False)


db.create_all()
