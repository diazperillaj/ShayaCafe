from flask import Blueprint, render_template, flash, redirect, url_for, make_response
from weasyprint import HTML
from app.models.sell import *
from app.forms.sell import *
from sqlalchemy.orm import aliased
import random
from app.models.tables_sells import sellsProcessedTable, sellsOthersTable, sellsProductsTable
from app.models.inventory import othersInInventory, processedCoffee, dryParchmentCoffee, Inventory, Category


sell = Blueprint('sell', __name__)

@sell.route('/')
def sells():

    orders_others = sellsOthersTable.return_all_sells()
    orders_processed = sellsProcessedTable().return_all_sells()
    orders_products = sellsProductsTable().return_all_sells()

    return render_template('sell/sell.html',
        orders_processed = orders_processed,
        orders_others = orders_others,
        orders_products = orders_products,
        products = Product.query.all())

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

@sell.route('/edit/product/<int:id>', methods=['GET','POST'])
def edit_product(id: int):
    
    try:
        product = Product.query.get(id)
        productF = productForm(obj=product)

        if productF.validate_on_submit():
            productF.populate_obj(product)
            db.session.commit()
            flash('Se ha editado con exito','completed')
            return redirect(url_for('sell.sells'))

    except Exception as e:
        flash('Error al editar edit_sell_product', 'error')
        print(e)

    return render_template('sell/product/productEdit.html',
        productForm = productF
        )

@sell.route('/delete/product/<int:id>', methods=['POST'])
def delete_product(id: int):

    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
        flash('Se ha eliminado con exito','completed')
    except Exception as e:
        flash('No se pudo eliminar, por favor verifique que no tiene compras relacionadas','error')
        print(e)

    return redirect(url_for('sell.sells'))

@sell.route('/create/sell/product', methods=['GET','POST'])
def create_sell_product():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.product_id.choices = [
        (product.id, f"{product.name}: {product.price}") for product in Product.query.all()
    ]

    if orderDetailF.product_id.choices == []:
        flash('Por favor agregar productos rapidos primero', 'error')
        return redirect(url_for('sell.sells'))

    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():

        try:

            product = Product.query.get(orderDetailF.product_id.data)
            
            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * product.price

            db.session.add(order)
            db.session.commit()

            orderDet.category_id = 4
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id
            orderDet.unit_price = product.price

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))
        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/product/sellCreateProduct.html',
        orderDetailForm = orderDetailF,
        orderForm = orderF)


@sell.route('/delete/sell/product/<int:id>', methods=['POST'])
def delete_sell_product(id: int):
    try:
        deleteSells(id, 4)
        flash('Se ha eliminado con exito, el producto a vuelto al inventario', 'completed')

    except Exception as e:
        print(e)
        flash('No se pudo eliminar','error')

@sell.route('/create/sell/other', methods=['GET','POST'])
def create_sell_other():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.product_id.choices = [
        (other.id, f"{other.name}: {other.price}, Cantidad: {inventory.quantity}")
        for other in othersInInventory.query.all()
            for inventory in Inventory.query.filter_by(product_id=other.id, category_id=3).all()
                if inventory.quantity > 0
    ]

    if orderDetailF.product_id.choices == []:
        flash('Por favor agregar "otros" primero', 'error')
        return redirect(url_for('sell.sells'))


    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():
        try:
            otherInven = Inventory.query.filter_by(product_id = orderDetailF.product_id.data, category_id = 3).first()

            
            if orderDetailF.quantity.data > otherInven.quantity:
                flash('No hay suficiente inventario', 'error')
                return redirect(url_for('sell.create_sell_other'))

            other = othersInInventory.query.get(orderDetailF.product_id.data)
            otherInven.quantity = otherInven.quantity - orderDetailF.quantity.data
            

            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * other.price

            db.session.add(order)
            db.session.commit()

            orderDet.category_id = 3
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id
            orderDet.unit_price = other.price

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))

        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/other/sellCreateOther.html',
        orderForm = orderF,
        orderDetailForm = orderDetailF)


@sell.route('/delete/sell/other/<int:id>', methods=['POST'])
def delete_sell_other(id: int):
    try:
        deleteSells(id, 3)
        flash('Se ha eliminado con exito, el producto a vuelto al inventario', 'completed')

    except Exception as e:
        print(e)
        flash('No se pudo eliminar','error')
    
    return redirect(url_for('sell.sells'))

@sell.route('/create/sell/processed-coffee', methods=['GET','POST'])
def create_sell_processed_coffee():

    order = Order()
    orderDet = orderDetail()

    orderF = orderForm()
    orderDetailF = orderDetailForm()

    orderDetailF.product_id.choices = [
        (processed.id, f"Lote: {processed.dry_parchment_coffee_id}-{processed.id}, Caficultor: {dryParchmentCoffee.query.get(processed.dry_parchment_coffee_id).farmer.name}, {processed.processed_category} {processed.weight} Kg, Precio: {processed.price}, Cantidad: {inventory.quantity}, Fecha: {inventory.entry_date}")
        for processed in processedCoffee.query.all()
            for inventory in Inventory.query.filter_by(product_id=processed.id, category_id=2).all()
                if inventory.quantity > 0
    ]
    
    if orderDetailF.product_id.choices == []:
        flash('Por favor agregar productos rapidos primero', 'error')
        return redirect(url_for('sell.sells'))

    if orderF.validate_on_submit() and orderDetailF.validate_on_submit():
        try:
            processed = Inventory.query.filter_by(product_id=orderDetailF.product_id.data, category_id=2).first()

            proce = processedCoffee.query.get(orderDetailF.product_id.data)

            if processed.quantity < orderDetailF.quantity.data:
                flash('No hay suficiente cantidad en el inventario','error')
                return redirect(url_for('sell.sells'))

            processed.quantity = processed.quantity - orderDetailF.quantity.data

            if processed.quantity == 0:
                flash(f'Ya no queda cafe procesado registrado con ID: {processed.product_id} en el inventario','terminated')
            
            orderF.populate_obj(order)
            orderDetailF.populate_obj(orderDet)

            order.sub_total = orderDetailF.quantity.data * proce.price

            db.session.add(order)
            db.session.commit()

            orderDet.category_id = 2
            orderDet.product_id = orderDetailF.product_id.data
            orderDet.order_id = order.id
            orderDet.unit_price = proce.price

            db.session.add(orderDet)
            db.session.commit()

            return redirect(url_for('sell.sells'))

        except Exception as e:
            flash('error','error')
            print(e)

    return render_template('sell/processed/sellCreateProcessed.html',
        orderForm = orderF,
        orderDetailForm = orderDetailF)

@sell.route('/delete/sell/processed/<int:id>', methods=['POST'])
def delete_sell_processed(id: int):
    try:
        deleteSells(id, 2)
        flash('Se ha eliminado con exito, el producto a vuelto al inventario', 'completed')

    except Exception as e:
        print(e)
        flash('No se pudo eliminar','error')
    
    return redirect(url_for('sell.sells'))


@sell.route('/auto/sells/<int:amount>', methods=['get'])
def auto_sells(amount: int):


    sells = sellsProcessedTable()

    # try:
    #     for i in range(amount):
    #         order = Order(
    #             sub_total = 0,
    #             order_date = datetime.datetime.now()
    #         )
            
    #         db.session.add(order)
    #         db.session.commit()

    #         choice = random.choice(processedCoffee.query.all())
    #         quant = random.randint(1, 10)

    #         orderDet = orderDetail(
    #             product_id = choice.id,
    #             category_id = 2,
    #             order_id = order.id,
    #             unit_price = choice.price,
    #             quantity = quant
    #         )

    #         order.sub_total = orderDet.unit_price * orderDet.quantity

    #         db.session.add(orderDet)
    #         db.session.commit()
    # except Exception as e:
    #     print(e)

    return redirect(url_for('sell.sells'))


def deleteSells(order_id:int, category_id: int):

    order = Order.query.get(order_id)
    orderDet = orderDetail.query.filter_by(order_id=order_id, category_id = category_id).first()

    if category_id != 4:
        inventory = Inventory.query.filter_by(product_id = orderDet.product_id, category_id = category_id).first()
        inventory.quantity += orderDet.quantity

    db.session.delete(order)
    db.session.delete(orderDet)
    db.session.commit()





@sell.route('/invoice/') 
def generate_invoice():
    
    orders_processed = sellsProcessedTable().return_all_sells()
    # Renderiza la plantilla con los datos
    order = 'Hola'

    print(f'Tamanio: {len(orders_processed)}')

    rendered = render_template('invoice.html', orders_processed=orders_processed, order=order)


    # Genera el PDF
    pdf = HTML(string=rendered).write_pdf()

    # Crea la respuesta para descargar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=invoice_{1}.pdf'
    
    return response
