from . import db
from sqlalchemy.orm import relationship

class Category(db.Model):

    # A category related with inventory, one category has many inventories

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(), nullable=False)
    inventories = relationship('Inventory', back_populates='category')

class Inventory(db.Model):

    # Inventory table
    # A inventory is related with category, an inventory has many categories

    """
        An inventory is related with category, (one to many)
    """

    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    observation = db.Column(db.String(), default='NA')
    category = relationship('Category', back_populates='inventories')


class dryParchmentCoffee(db.Model):

    # Dry parchment coffee is related with farmers, a dry parchment
    # has one farmer and one farmer has many dry parchment

    # Dry parche

    __tablename__ = 'dry_parchment_coffees'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    variety = db.Column(db.String(200), nullable=False)
    altitude =  db.Column(db.Float, nullable=False)
    processed = db.Column(db.Boolean, nullable=False)

    # Relation with farmers (many to one)
    farmer = relationship('farmers', back_populates='dry_parchment_coffees')

    # Relation with processed_coffes (one to many)
    processed_coffes = relationship('processed_coffess', back_populates='dry_parchment_coffe')

class processedCoffee(db.Model):

    # A processed coffee has the weigh (must be in kg), the processed
    # category (Grano, molido) the processing date, who is responsible
    # of the process and an observation

    # Is related with dry parchment, one dry parchment may have many
    # process, and a processed has one dry parchment

    __tablename__ = 'processed_coffees'
    id = db.Column(db.Integer, primary_key=True)
    dry_parchment_coffee_id = db.Column(db.Integer, db.ForeignKey('dry_parchment_coffees.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    weight = db.Column(db.Float, nullable=False)
    processed_category = db.Column(db.String(120), nullable=False)
    processing_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    responsible = db.Column(db.String(120), nullable=False)
    observation = db.Column(db.String, nullable=False)

    # Relation with dry_parchment_coffees (many to one)
    dry_parchment_coffee = relationship('dry_parchment_coffee', back_populates='processedCoffes')


class othersInInventory(db.Model):
    __tablename__ = 'others_in_inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String, nullable=False)