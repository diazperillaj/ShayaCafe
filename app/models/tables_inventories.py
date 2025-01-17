from app import db
from app.models.inventory import Inventory, Category, dryParchmentCoffee, processedCoffee, othersInInventory
from datetime import datetime
from typing import List

class Base:
    def __init__(self, id = None, quantity = None, date = None, observation = None):

        self.id = id
        self.quantity = quantity
        self.date = self.format_date(date)
        self.observation = observation
    
    def format_date(self, date):
        return date.strftime('%Y-%m-%d') if date and isinstance(date, datetime) else None
    
class dryParchmentCoffeeTable(Base):
    def __init__(self, id = None, quantity = None, date = None, observation = None,
                farmer_name = None, altitude = None, variety = None):
        
        super().__init__(id, quantity, date, observation)

        self.farmer_name = farmer_name
        self.altitude = altitude
        self.variety = variety

    @classmethod
    def return_all_inventories(cls) -> List['dryParchmentCoffeeTable']:
        
        inventories = []

        query = (db.session.query(Inventory, dryParchmentCoffee)
                .filter(Inventory.category_id == 1)
                .join(dryParchmentCoffee, Inventory.product_id == dryParchmentCoffee.id))


        for inve, parchment in query.all():
            parchment = cls(
                id = parchment.id,
                farmer_name = parchment.farmer.name,
                variety = parchment.variety,
                altitude = parchment.altitude,
                quantity = inve.quantity,
                date = inve.entry_date,
                observation = inve.observation if inve.observation != '' else '-'
            )
            inventories.append(parchment)
        return inventories


class processedCoffeeTable(Base):
    def __init__(self, id = None, quantity = None, date = None, observation = None,
                parchment_id= None, farmer_name = None, weight = None, category = None,
                responsible = None, parchment_weight = None, total_weight = None,
                price = None, total_price = None):
        
        super().__init__(id, quantity, date, observation)

        self.parchment_id = parchment_id
        self.farmer_name = farmer_name
        self.weight = weight
        self.category = category
        self.responsible = responsible
        self.parchment_weight = parchment_weight
        self.total_weight = quantity * weight
        self.price = price
        self.total_price = quantity * price

    @classmethod
    def return_all_inventories(cls) -> List['processedCoffeeTable']:

        inventories = []

        query = (db.session.query(Inventory, processedCoffee, dryParchmentCoffee)
                .filter(Inventory.category_id == 2)
                .join(processedCoffee, Inventory.product_id == processedCoffee.id)
                .join(dryParchmentCoffee, processedCoffee.dry_parchment_coffee_id == dryParchmentCoffee.id))

        for inve, processed, parchment in query.all():
            processed = cls(
                id = processed.id,
                parchment_id = processed.dry_parchment_coffee_id,
                farmer_name = parchment.farmer.name,
                weight = processed.weight,
                category = processed.processed_category,
                responsible = processed.responsible,
                parchment_weight = processed.processed_parchment_weight,
                quantity = inve.quantity,
                date = inve.entry_date,
                observation = inve.observation if inve.observation != '' else '-',
                price = processed.price,
                total_price = processed.total_price
            )
            inventories.append(processed)
        return inventories
    
class othersInInventoryTable(Base):

    def __init__(self, id = None, name = None, quantity = None, date = None, observation = None):

        super().__init__(id, quantity, date, observation)
        self.name = name

    @classmethod
    def return_all_inventories(cls) -> List['othersInInventoryTable']:
        
        inventories = []

        query = (db.session.query(Inventory, othersInInventory)
                .filter(Inventory.category_id == 3)
                .join(othersInInventory, Inventory.product_id == othersInInventory.id))

        for inve, other in query.all():
            other = cls(
                id = other.id,
                name = other.name,
                quantity = inve.quantity,
                date = inve.entry_date,
                observation = inve.observation if inve.observation != '' else '-'
            )
            inventories.append(other)
        return inventories

