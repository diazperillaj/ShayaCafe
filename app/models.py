from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    products = db.relationship('Products', back_populates='category', lazy=True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    category = db.relationship('Categories', back_populates='products', lazy=True)

    inventory = db.relationship('Inventories', back_populates='product', uselist=False, lazy=True)

    sales = db.relationship('Sales', back_populates='product', lazy=True)
    

class Inventories(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False)
    product = relationship('Products', back_populates='inventory', lazy=True, uselist=False)

    __table_args__ = (
        db.UniqueConstraint('product_id', name='unique_product'),
    )

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET DEFAULT'), nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())


    product = db.relationship('Products', back_populates='sales', lazy=True)