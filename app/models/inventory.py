from app import db
from sqlalchemy.orm import relationship

class Category(db.Model):

    """
        The category are related with inventory (one to many)
    """

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False, default="NA")

    # Relation with inventories, (one to many)
    inventories = relationship('Inventory', back_populates='category')

class Inventory(db.Model):

    """
        Inventory:
            category_id: Used to separate the inventory in different categories,
                for example 'Dry parchment coffee', 'Processed coffee', 'Others'

            product_id: Is the id of the product related in category_id, for example:
                category_id = 1 (Dry Parchment Coffee)
                product_id = 1 (The product with the id 1 who belongs to dry parchment coffee category/table)
            
            quantity: The amount of product in the inventory, must be specified here beacause in the
                other tables are not the amount of the product in the columns

        Relations:
            An inventory is related with category, (many to one)
    """

    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    observation = db.Column(db.Text, default='NA')

    # Relation with categories, (many to one)
    category = relationship('Category', back_populates='inventories')


class dryParchmentCoffee(db.Model):

    """
        Dry parchment coffee:
            farmer_id: Is the farmer who owns the coffee (FOREIGN KEY RELATED TO farmers.id)

            variety: Is the variety of the coffee, for example "Arabica, caturra, etc"
            
            processed: Type boolean, is used when a complete dry parchment coffee is processed,
                it change status to true

        Relations:
            Dry parchment coffee is related with farmes, (many to one)
            Dry parchment coffee is related with processed_coffees, (one to many)
    """

    __tablename__ = 'dry_parchment_coffees'
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    variety = db.Column(db.String(200), nullable=False)
    altitude =  db.Column(db.Float, nullable=False)
    processed = db.Column(db.Boolean, nullable=False)
    observation = db.Column(db.Text, nullable=False, default="NA")

    # Relation with farmers (many to one)
    farmer = relationship('Farmer', back_populates='dry_parchment_coffees')

    # Relation with processed_coffes (one to many)
    processed_coffes = relationship('processedCoffee', back_populates='dry_parchment_coffee')

class processedCoffee(db.Model):

    """
        Processed coffee:
            weight: Must be the weight of the individualy processed coffee bags, for example:
                If there are 200 Kg of toasted coffee separated in 200 bags of 1Kg each one,
                the individual weight must be specified here (1 Kg), the 200 must be
                in inventories.quantity

            processed_category: May be "Grano, molido, etc"

            responsible: Is the person or company who make the process
        
            
        Relations:    
            processed_coffees are related with dry_parchment_coffes (many to one)    
    """

    __tablename__ = 'processed_coffees'
    id = db.Column(db.Integer, primary_key=True)
    dry_parchment_coffee_id = db.Column(db.Integer, db.ForeignKey('dry_parchment_coffees.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    weight = db.Column(db.Float, nullable=False)
    processed_category = db.Column(db.String(120), nullable=False)
    responsible = db.Column(db.String(120), nullable=False)
    
    # Relation with dry_parchment_coffees (many to one)
    dry_parchment_coffee = relationship('dryParchmentCoffee', back_populates='processed_coffes')


class othersInInventory(db.Model):

    """
        Other in inventory are third things wich are in the inventory, for example objects to
        prepare coffee like glasses
    """

    __tablename__ = 'others_in_inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False, default="NA")