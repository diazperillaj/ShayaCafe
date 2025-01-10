from flask import Blueprint, render_template, flash, redirect, url_for
from app.models.sell import *
from app.forms.sell import *
from sqlalchemy.orm import aliased
from app.models.inventory import othersInInventory, processedCoffee, dryParchmentCoffee, Inventory, Category


sell = Blueprint('sell', __name__)

@sell.route('/')
def sells():

    orders = Order.query.all()
    order_details = orderDetail.query.all()

    processed = processedCoffee.query.all()
    others = othersInInventory.query.all()
    products = Product.query.all()

    return render_template('sell/sell.html',
        products = products,
        orders = orders,
        order_details = order_details,
        processed = processed,
        others = others)

@sell.route('/create/sell')
def create_sell():
    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.category_id.choices = [
        (category.id, category.name) for category in Category.query.all()
    ]

    return render_template('sell/sellCreate.html',
        orderForm = orderF,
        orderDetailForm = orderDetailF)

@sell.route('/create/product', methods=['GET','POST'])
def create_product():
    productF = productForm()
    product = Product()

    if productF.validate_on_submit():
        try:
            
            productF.populate_obj(product)
            
            db.session.add(product)
            db.session.commit()

            flash('Se ha agregado con exito','completed')
            return redirect(url_for('sell.sells'))

        except Exception as e:
            flash('Error','error')
            print(e)
            return redirect(url_for('sell.create_product'))

    return render_template('sell/product/productCreate.html', productForm = productF)


@sell.route('/create/sell/product', methods=['GET','POST'])
def create_sell_product():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.product_id.choices = [
        (product.id, f"{product.name}: {product.price}") for product in Product.query.all()
    ]

    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():

        try:
            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * Product.query.get(orderDetailF.product_id.data).price

            db.session.add(order)
            db.session.commit()


            orderDet.category_id = 4
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))
        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/product/sellCreateProduct.html',
        orderDetailForm = orderDetailF,
        orderForm = orderF)



@sell.route('/create/sell/other', methods=['GET','POST'])
def create_sell_other():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.product_id.choices = [
        (other.id, f"{other.name}: {other.price}") for other in othersInInventory.query.all()
    ]

    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():
        try:
            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * othersInInventory.query.get(orderDetailF.product_id.data).price

            db.session.add(order)
            db.session.commit()

            orderDet.category_id = 3
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))

        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/other/sellCreateOther.html',
        orderForm = orderF,
        orderDetailForm = orderDetailF)



@sell.route('/create/sell/processed-coffee', methods=['GET','POST'])
def create_sell_processed_coffee():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()


    inventory_alias = aliased(Inventory)


    processed_with_inventory = (
        db.session.query(
            processedCoffee.id,
            processedCoffee.dry_parchment_coffee_id,
            processedCoffee.processed_category,
            processedCoffee.price,
            inventory_alias.entry_date,
            inventory_alias.quantity,
        )
        .join(inventory_alias, inventory_alias.product_id == processedCoffee.dry_parchment_coffee_id)
        .filter(inventory_alias.category_id == 2)
        .all()
    )

    orderDetailF.product_id.choices = [
        (
            item.id,
            f"ID: {item.id}, ID Pergamino: {item.dry_parchment_coffee_id}, "
            f"Fecha: {item.entry_date}, Tipo proceso: {item.processed_category}, "
            f"Precio: {item.price}, Cantidad: {item.quantity}"
        )
        for item in processed_with_inventory
    ]




    # orderDetailF.product_id.choices = [
    #     (other.id, f"ID: {other.id}, ID Pergamino: {other.dry_parchment_coffee_id}, Fecha: {inventory.entry_date}, Tipo proceso: {other.processed_category}, Precio:{other.price}, Cantidad: {inventory.quantity}")
    #     for other in processedCoffee.query.all()
    #         for inventory in Inventory.query.filter_by(product_id=other.dry_parchment_coffee_id, category_id=2)
    # ]

    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():
        try:
            processed = Inventory.query.filter_by(product_id=orderDetailF.product_id.data, category_id=2).first()

            if processed.quantity < orderDetailF.quantity.data:
                flash('No hay suficiente cantidad en el inventario','error')
                return redirect(url_for('sell.sells'))

            processed.quantity = processed.quantity - orderDetailF.quantity.data

            if processed.quantity == 0:
                flash(f'Ya no queda cafe procesado registrado con ID: {processed.product_id} en el inventario','terminated')
            
            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * processedCoffee.query.get(orderDetailF.product_id.data).price

            db.session.add(order)
            db.session.commit()

            orderDet.category_id = 2
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))

        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/processed/sellCreateProcessed.html',
        orderForm = orderF,
        orderDetailForm = orderDetailF)