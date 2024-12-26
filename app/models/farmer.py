from app import db
from sqlalchemy.orm import relationship

class Farmers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    farm_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    observation = db.Column(db.Text, nullable=False, default='NA')