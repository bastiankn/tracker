from extensions import db
from models.user_model import User
from datetime import datetime

class Weight(db.Model):
    __tablename__='weight'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) # maybe that needs changing
    weight = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=True)
    total_body_water = db.Column(db.Float, nullable=True)
    muscle_mass = db.Column(db.Float, nullable=True)
    bone_density = db.Column(db.Float, nullable=True)

    user = db.relationship('User', backref='weights')