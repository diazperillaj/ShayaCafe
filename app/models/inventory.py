from . import db
from sqlalchemy.orm import relationship

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(), nullable=False)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories', ondelete='SET DEFAULT'), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    observation = db.Column(db.String(), default='NA')

class dryParchmentCoffee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers', ondelete='SET DEFAULT'), nullable=False, default=0)
    variety = db.Column(db.String(200), nullable=False)
    altitude =  db.Column(db.Float, nullable=False)
    processed = db.Column(db.Boolean, nullable=False)

class processedCoffee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    processed_category = db.Column(db.String(120), nullable=False)
    processing_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    responsible = db.Column(db.String(120), nullable=False)
    observation = db.Column(db.String, nullable=False)

class othersInInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String, nullable=False)