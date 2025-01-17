from app.models.sell import Order, orderDetail, Product
from app import db
from datetime import datetime
from app.models.inventory import dryParchmentCoffee, processedCoffee, othersInInventory
from typing import List


"""
    Base sell is the base class for all sells, have a format_date method to format the date

    In all class, the common is do a for in the query and create objects, then this objects are
    added to the returned list

"""

def parse_number(number: int):
    return f'{number:04d}'

class BaseSell:
    def __init__(self, id=None, price=None, quantity=None,
                 sub_total=None, date=None, observation=None):
        self.id = id
        self.price = price
        self.quantity = quantity
        self.sub_total = sub_total
        self.date = self.format_date(date)
        self.observation = observation

    def format_date(self, date):
        return date.strftime('%Y-%m-%d') if date and isinstance(date, datetime) else None


class sellsProcessedTable(BaseSell):
    def __init__(self, id=None, processed_id=None, parchment_id=None, farmer_name=None,
                category=None, weight=None, price=None, quantity=None, 
                sub_total=None, date=None, observation=None):
        super().__init__(id, price, quantity, sub_total, date, observation)
        self.processed_id = processed_id
        self.parchment_id = parchment_id
        self.farmer_name = farmer_name
        self.category = category
        self.weight = weight

    @classmethod
    def return_all_sells(cls) -> List['sellsProcessedTable']:
        sellsProcessedCoffees = []

        query = (db.session.query(orderDetail, Order, processedCoffee, dryParchmentCoffee)
                .filter(orderDetail.category_id == 2)
                .join(Order, orderDetail.order_id == Order.id)
                .join(processedCoffee, orderDetail.product_id == processedCoffee.id)
                .join(dryParchmentCoffee, processedCoffee.dry_parchment_coffee_id == dryParchmentCoffee.id)
                .order_by(Order.order_date.desc()))

        for orderDet, order, processed, parchment in query.all():
            sellsTable = cls(
                            id = parse_number(order.id),
                            processed_id = orderDet.product_id,
                            parchment_id = processed.dry_parchment_coffee_id,
                            farmer_name =  parchment.farmer.name,
                            category = processed.processed_category,
                            weight = processed.weight,
                            price = orderDet.unit_price,
                            quantity = orderDet.quantity,
                            sub_total = order.sub_total,
                            date = order.order_date,
                            observation = order.observation
                        )
            sellsProcessedCoffees.append(sellsTable)

        return sellsProcessedCoffees

class sellsOthersTable(BaseSell):
    def __init__(self, id=None, name=None, price=None, quantity=None,
                sub_total=None, date=None, observation=None):
        super().__init__(id, price, quantity, sub_total, date, observation)
        self.name = name

    @classmethod
    def return_all_sells(cls) -> List['sellsOthersTable']:
        sellsOthers = []

        query = (db.session.query(orderDetail, Order, othersInInventory)
                .filter(orderDetail.category_id == 3)
                .join(Order, orderDetail.order_id == Order.id)
                .join(othersInInventory, orderDetail.product_id == othersInInventory.id)
                )

        for orderDet, order, other in query.all():
            sellsTable = cls(
                            id = order.id,
                            name = other.name,
                            price = orderDet.unit_price,
                            quantity = orderDet.quantity,
                            sub_total = order.sub_total,
                            date = order.order_date,
                            observation = order.observation
                        )
            sellsOthers.append(sellsTable)

        return sellsOthers

class sellsProductsTable(BaseSell):
    def __init__(self, id=None, name=None, price=None, quantity=None,
                sub_total=None, date=None, observation=None):
        super().__init__(id, price, quantity, sub_total, date, observation)
        self.name = name
    
    @classmethod
    def return_all_sells(cls) -> List['sellsProductsTable']:

        sellsProducts = []

        query = (db.session.query(orderDetail, Order, Product)
                .filter(orderDetail.category_id == 4)
                .join(Order, orderDetail.order_id == Order.id)
                .join(Product, orderDetail.product_id == Product.id))
        
        print(f'Tamanio: {len(query.all())}')

        for orderDet, order, product in query.all():
            sellsTable = cls(
                            id = order.id,
                            name = product.name,
                            price = orderDet.unit_price,
                            quantity = orderDet.quantity,
                            sub_total = order.sub_total,
                            date = order.order_date,
                            observation = order.observation
                        )
            sellsProducts.append(sellsTable)

        return sellsProducts
    
