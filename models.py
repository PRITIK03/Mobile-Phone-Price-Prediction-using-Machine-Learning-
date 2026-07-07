from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    battery_size = db.Column(db.Float, nullable=False)
    brand_name = db.Column(db.String(50), nullable=False)
    memory_size = db.Column(db.Float, nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    lowest_price = db.Column(db.Float, nullable=False)
    highest_price = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    screen_size = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('predictions', lazy=True))
