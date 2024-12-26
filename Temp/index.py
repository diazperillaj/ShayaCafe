from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    return render_template('index.html')

@views.route('/product')
@login_required
def inventory():
    products = Products.query.all()
    return render_template('showInventory.html', products=products)

@views.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_inventory():

    form = productForm()

    form.product.choices = [
            (product.id, product.name) for product in Products.query.all()
        ]
    form.category.choices = [
            (category.id, category.name) for category in Categories.query.all()
    ]

    if form.validate_on_submit():
        product = Products.query.filter_by(name=form.name.data.capitalize(), category=form.category.data.capitalize()).first()

        if product:

            if form.option.data == '1':
                product.quantity += int(form.quantity.data)
                if product.price != int(form.price.data):
                    product.price = int(form.price.data)
            else:
                product.quantity -= int(form.quantity.data)
        
        else:
            product = Products(name=form.name.data.capitalize().strip(), category=form.category.data.capitalize().strip(), quantity=int(form.quantity.data), price=int(form.price.data))
            db.session.add(product)
        
        db.session.commit()
        flash('Añadido al inventario', 'success')
        return redirect(url_for('views.inventory'))

    return render_template('addInventory.html', form=form)

@views.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    sales = Sales.query.all()
    return render_template('showSales.html', sales=sales)


@views.route('/add-sale', methods=['GET', 'POST'])
@login_required
def add_sale():
    form=salesForm()

    if form.validate_on_submit():

        quantity = form.quantity.data
        price = form.price.data

        sale = Sales(name=form.name.data.capitalize().strip(),
                    category=form.category.data.capitalize().strip(),
                    quantity=int(form.quantity.data), 
                    price=int(form.price.data),
                    totalPrice=int(form.quantity.data) * int(form.price.data),
                    date=form.date.data)
        
        db.session.add(sale)
        db.session.commit()
        return redirect(url_for('views.sales'))

    return render_template('addSale.html', form=form)