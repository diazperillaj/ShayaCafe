from app import db
from sqlalchemy.orm import relationship

class Farmer(db.Model):

    """
        Farmers are related with dry_parchment_coffees, (one to many)
    """

    __tablename__ = 'farmers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    farm_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    observation = db.Column(db.Text, nullable=False, default='NA')

    # Relatio with dry_parchment_coffees, (one to many)
    dry_parchment_coffees = relationship('dryParchmentCoffee', back_populates='farmer')