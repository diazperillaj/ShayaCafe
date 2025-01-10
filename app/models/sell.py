from app import db
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    sub_total  = db.Column(db.Float, nullable=False)
    order_date  = db.Column(db.DateTime, nullable=False)
    observation = db.Column(db.Text, nullable=True, default='NA')

    # Relationship with orderDetail (one to many)
    order_details = relationship('orderDetail', back_populates='order')

class orderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer, nullable=False)

    # Relationship with Order (many to one)
    order = relationship('Order', back_populates='order_details')

