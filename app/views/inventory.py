from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms.inventory import *
from app.models.inventory import *
from app.models.farmer import Farmer


inventoryViews = Blueprint('inventoryViews', __name__)



@inventoryViews.route('/')
def inventory():
    inv = Inventory.query.all()

    dry_parchment_inv = dryParchmentCoffee.query.all()
    processed_inv = processedCoffee.query.all()
    others_inv = othersInInventory.query.all()

    return render_template('inventory/inventory.html',
        inventories = inv,
        dry_parchment_coffees = dry_parchment_inv,
        processed_coffees = processed_inv,
        others_in_inventories = others_inv
    )



@inventoryViews.route('/create/category', methods=['GET','POST'])
def inventory_create_category():
    form = categoryForm()

    if form.validate_on_submit():
        cate = Category(name=form.name.data.capitalize(), description=form.description.data)
        try:
            db.session.add(cate)
            db.session.commit()
            return redirect(url_for('inventoryViews.inventory'))
        except:
            pass

    return render_template('inventory/category/inventoryCreateCategory.html', form=form)



@inventoryViews.route('/create/dry-parchment-coffee', methods=['GET','POST'])
def inventory_create_dry_parchment_coffee():

    inventoryF = inventoryForm()
    dryParchmentCoffeeF = dryParchmentCoffeeForm()

    dryParchmentCoffeeF.farmer_id.choices = [
                        (farmer.id, farmer.name) for farmer in Farmer.query.all()
                        ]
    
    if dryParchmentCoffeeF.validate_on_submit():
        try:
            dryParchment = dryParchmentCoffee(
                farmer_id = dryParchmentCoffeeF.farmer_id.data,
                variety = dryParchmentCoffeeF.variety.data.capitalize(),
                altitude = dryParchmentCoffeeF.altitude.data,
                processed = False,
                price = dryParchmentCoffeeF.price.data)
            db.session.add(dryParchment)
            db.session.commit()
            
            
            inventoryF.category_id.data = 1
            inventoryF.product_id.data = dryParchment.id

            if inventoryF.validate_on_submit():
                inventoryModel = Inventory(
                    category_id = inventoryF.category_id.data,
                    product_id = inventoryF.product_id.data,
                    quantity = inventoryF.quantity.data,
                    entry_date = inventoryF.entry_date.data,
                    observation = inventoryF.observation.data,
                )

                db.session.add(inventoryModel)
                db.session.commit()
                return redirect(url_for('inventoryViews.inventory'))
        except Exception as e:
            flash('No se ha podido completar', 'error')
            print(e)
            

    return render_template('inventory/dry_parchment/inventoryCreateDryParchmentCoffee.html',
                        inventoryForm=inventoryF,
                        dryParchmentCoffeeForm=dryParchmentCoffeeF)


@inventoryViews.route('/edit/dry-parchment-coffee/<int:parchment_id>', methods=['GET','POST'])
def inventory_edit_dry_parchment_coffee(parchment_id: int):
    
    inventory = Inventory.query.filter_by(product_id=parchment_id, category_id=1).first()
    dryParchament = dryParchmentCoffee.query.get(parchment_id)

    inventoryF = inventoryForm(obj=inventory)
    dryParchmentF = dryParchmentCoffeeForm(obj=dryParchament)

    dryParchmentF.farmer_id.choices = [
                        (farmer.id, farmer.name) for farmer in Farmer.query.all()
                        ]
    
    if dryParchmentF.validate_on_submit():
        try:
            inventoryF.populate_obj(inventory)
            dryParchmentF.populate_obj(dryParchament)

            db.session.commit()

            return redirect(url_for('inventoryViews.inventory'))
        
        except Exception as e:
            flash('Error','error')
            print(e)
        

    return render_template('inventory/dry_parchment/inventoryEditDryParchmentCoffee.html',
        inventoryForm=inventoryF,
        dryParchmentCoffeeForm=dryParchmentF)



@inventoryViews.route('/delete/dry-parchment-coffee/<int:parchment_id>', methods=['POST'])
def inventory_delete_dry_parchment_coffee(parchment_id: int):

    dry_parchment = dryParchmentCoffee.query.get(parchment_id)
    inve = Inventory.query.filter_by(product_id=parchment_id, category_id=1).first()

    if not dry_parchment:
        flash('Error','error')
        return redirect(url_for('inventoryViews.inventory'))

    try:
        db.session.delete(dry_parchment)
        db.session.delete(inve)
        db.session.commit()
    except Exception as e:
        flash('No se ha podido eliminar, por favor revisa que no tenga cafes procesados registrados con este id','error')
        print('Error', e)

    return redirect(url_for('inventoryViews.inventory'))



@inventoryViews.route('/create/processed-coffee', methods=['GET','POST'])
def inventory_create_processed_coffee():

    """
        'inventoryF' and 'processedCoffeeF' get the forms of that models
    """

    inventoryF = inventoryForm()
    processedCoffeeF = processedCoffeeForm()

    processedCoffeeF.dry_parchment_coffee_id.choices = [ 
        (dry_parchment_coffee.id,f"ID: {dry_parchment_coffee.id}, Fecha: {Inventory.query.filter_by(product_id=dry_parchment_coffee.id).first().entry_date}, Caficultor: {dry_parchment_coffee.farmer.name}")
        for dry_parchment_coffee in dryParchmentCoffee.query.all()]

    if not dryParchmentCoffee.query.all():
        flash('Se debe agregar pergamino seco antes de registrar un cafe procesado', 'error')
        return redirect(url_for('inventoryViews.inventory'))

    if processedCoffeeF.validate_on_submit():
        print('Entra')
        try:
            processedModel = processedCoffee(
                dry_parchment_coffee_id = processedCoffeeF.dry_parchment_coffee_id.data,
                weight = processedCoffeeF.weight.data,
                processed_category = processedCoffeeF.processed_category.data.capitalize(),
                responsible = processedCoffeeF.responsible.data.capitalize(),
                price = processedCoffeeF.price.data,
                total_price = processedCoffeeF.price.data * inventoryF.quantity.data
            )

            db.session.add(processedModel)
            db.session.commit()

            inventoryF.category_id.data = 2
            inventoryF.product_id.data = processedModel.id

            if inventoryF.validate_on_submit():

                inventoryModel = Inventory(
                    category_id = inventoryF.category_id.data,
                    product_id = inventoryF.product_id.data,
                    quantity = inventoryF.quantity.data,
                    entry_date = inventoryF.entry_date.data,
                    observation = inventoryF.observation.data,
                )

                db.session.add(inventoryModel)
                db.session.commit()

                return redirect(url_for('inventoryViews.inventory'))

        except Exception as e:
            flash('No se ha podido completar', 'error')
            print(e)
        

    return render_template('inventory/processed/inventoryCreateProcessedCoffee.html',
        inventoryForm=inventoryF,
        processedCoffeeForm=processedCoffeeF, temp=inventory)


@inventoryViews.route('/edit/processed-coffee/<int:processed_id>', methods=['GET', 'POST'])
def inventory_edit_processed_coffee(processed_id: int):
    
    inventory = Inventory.query.filter_by(product_id=processed_id, category_id=2).first()
    processed = processedCoffee.query.get(processed_id)

    inventoryF = inventoryForm(obj=inventory)
    processedCoffeeF = processedCoffeeForm(obj=processed)

    processedCoffeeF.dry_parchment_coffee_id.choices = [ 
    (dry_parchment_coffee.id,f"ID: {dry_parchment_coffee.id}, Fecha: {Inventory.query.filter_by(product_id=dry_parchment_coffee.id).first().entry_date}, Caficultor: {dry_parchment_coffee.farmer.name}")
    for dry_parchment_coffee in dryParchmentCoffee.query.all()]

    if request.method == 'POST':
        try:

            if processedCoffeeF.validate_on_submit():
                inventoryF.populate_obj(inventory)
                processedCoffeeF.populate_obj(processed)

                inventory.total_price = processedCoffeeF.price.data * inventoryF.quantity.data

                db.session.commit()

                return redirect(url_for('inventoryViews.inventory'))

        except Exception as e:
            flash('Error, no se ha podido completar la actualizacion','error')
            print(e)

    return render_template('inventory/processed/inventoryEditProcessedCoffee.html',
        inventoryForm=inventoryF,
        processedCoffeeForm=processedCoffeeF)


@inventoryViews.route('/delete/processed/<int:processed_id>', methods=['POST'])
def inventory_delete_processed_coffee(processed_id: int):
    
    processed = processedCoffee.query.get(processed_id)
    inve = Inventory.query.filter_by(product_id=processed_id, category_id=2).first()

    if not processed:
        return redirect(url_for('inventoryViews.inventory'))

    try:
        db.session.delete(processed)
        db.session.delete(inve)
        db.session.commit()
    except Exception as e:  
        flash('Error','error')

    return redirect(url_for('inventoryViews.inventory'))


@inventoryViews.route('/create/others-in-inventory', methods=['GET','POST'])
def inventory_create_others_in_inventory():

    inventoryF = inventoryForm()
    othersInInventoryF = othersInInventoryForm()

    if othersInInventoryF.validate_on_submit():
        try:

            othersInInventoryModel = othersInInventory(
                name = othersInInventoryF.name.data.capitalize(),
                price = othersInInventoryF.price.data,
                description = othersInInventoryF.name.data.capitalize()
            )

            db.session.add(othersInInventoryModel)
            db.session.commit()

            inventoryF.category_id.data = 3
            inventoryF.product_id.data = othersInInventoryModel.id

            if inventoryF.validate_on_submit():

                inventoryModel = Inventory(
                    category_id = inventoryF.category_id.data,
                    product_id = inventoryF.product_id.data,
                    quantity = inventoryF.quantity.data,
                    entry_date = inventoryF.entry_date.data,
                    observation = inventoryF.observation.data,
                )

                db.session.add(inventoryModel)
                db.session.commit()

                return redirect(url_for('inventoryViews.inventory'))

        except Exception as e:
            flash('No se ha podido completar', 'error')
            print(e)

    return render_template('inventory/other/inventoryCreateOthers.html',
                        inventoryForm=inventoryF,
                        othersInInventoryForm=othersInInventoryF)

@inventoryViews.route('/edit/others-in-inventory/<int:others_id>', methods=['GET', 'POST'])
def inventory_edit_others_in_inventory(others_id: int):

    inventory = Inventory.query.filter_by(product_id=others_id, category_id=3).first()
    othersInInv = othersInInventory.query.get(others_id)

    inventoryF = inventoryForm(obj=inventory)
    othersInInventoryF = othersInInventoryForm(obj=othersInInv)

    if request.method == 'POST':
        try:
            if inventoryF.validate_on_submit():
                inventoryF.populate_obj(inventory)
                othersInInventoryF.populate_obj(othersInInv)

                db.session.commit()

                return redirect(url_for('inventoryViews.inventory'))

        except Exception as e:
            flash('No se ha podido completar', 'error')
            print(e)


    return render_template('inventory/other/inventoryEditOthers.html',
        inventoryForm=inventoryF,
        othersInInventoryForm=othersInInventoryF)

@inventoryViews.route('/delete/others-in-inventory/<int:others_id>', methods=['POST'])
def inventory_delete_others_in_inventory(others_id: int):
    
    otherInve = othersInInventory.query.get(others_id)
    inve = Inventory.query.filter_by(product_id=others_id, category_id=3).first()

    if not otherInve:
        return redirect(url_for('inventoryViews.inventory'))

    try:
        db.session.delete(otherInve)
        db.session.delete(inve)
        db.session.commit()
    except Exception as e:  
        flash('Error','error')

    return redirect(url_for('inventoryViews.inventory'))