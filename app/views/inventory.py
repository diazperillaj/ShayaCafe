from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms.inventory import *
from app.models.inventory import *
from app.models.farmer import Farmer
from app.models.tables_inventories import dryParchmentCoffeeTable, processedCoffeeTable,othersInInventoryTable


inventoryViews = Blueprint('inventoryViews', __name__)



@inventoryViews.route('/')
def inventory():

    inventories_parchments = dryParchmentCoffeeTable.return_all_inventories()
    inventories_processed = processedCoffeeTable.return_all_inventories()
    inventories_others = othersInInventoryTable.return_all_inventories()
    inventories = Inventory.query.all()

    return render_template('inventory/inventory.html',
        inventories_parchments = inventories_parchments,
        inventories_processed = inventories_processed,
        inventories_others = inventories_others,
        inventories = inventories
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
                inventoryModel = Inventory()
                inventoryF.populate_obj(inventoryModel)

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

    """
        'dryParch' get all the dry parchment coffees and is used to create the 'dry_parchment_coffee_id' choices\
        and validate if there are dry parchment coffees
    """

    dryParch = dryParchmentCoffee.query.all()

    processedCoffeeF.dry_parchment_coffee_id.choices = [ 
        (dry_parchment_coffee.id,f"ID: {dry_parchment_coffee.id}, {inventory.quantity} Kg, Fecha: {inventory.entry_date}, Caficultor: {dry_parchment_coffee.farmer.name}")
        for dry_parchment_coffee in dryParch
            for inventory in Inventory.query.filter_by(product_id=dry_parchment_coffee.id, category_id=1).all()
                if inventory.quantity > 0]

    if processedCoffeeF.dry_parchment_coffee_id.choices == []:
        flash('Se debe agregar pergamino seco antes de registrar un cafe procesado', 'error')
        return redirect(url_for('inventoryViews.inventory'))

    if processedCoffeeF.validate_on_submit():
        try:

            """
                Converting the form to object, and added the processed category and responsible capitalized.
            """

            processedModel = processedCoffee()
            processedCoffeeF.populate_obj(processedModel)

            processedModel.processed_category = processedModel.processed_category.capitalize(),
            processedModel.responsible = processedModel.responsible.title(),

            """
                Getting the total price of the processed coffee
            """
            processedModel.total_price = processedCoffeeF.price.data * inventoryF.quantity.data

            inventoryParchmentToModify = Inventory.query.filter_by(product_id=processedModel.dry_parchment_coffee_id, category_id=1).first()
            parchment = dryParchmentCoffee.query.get(processedModel.dry_parchment_coffee_id)


            if inventoryParchmentToModify.quantity < processedModel.processed_parchment_weight:
                flash('No hay suficiente inventario', 'error')
                return redirect(url_for('inventoryViews.inventory_create_processed_coffee'))

            inventoryParchmentToModify.quantity = inventoryParchmentToModify.quantity - processedModel.processed_parchment_weight

            parchment.processed = True if inventoryParchmentToModify.quantity == 0 else False

            db.session.add(processedModel)
            db.session.commit()

            """
                The inventoryForm set the category_id to 2 (Processed Coffee) and the product_id
                is the same as the processedModel.id (From table processed_coffees.id)

                If this 2 lines are deleted, it will not be possible to add processed coffees because
                the form detects the category_id and the product_id are empty because it has not
                this fields in the form
            """

            inventoryF.category_id.data = 2
            inventoryF.product_id.data = processedModel.id

            if inventoryF.validate_on_submit():

                inventoryModel = Inventory()
                inventoryF.populate_obj(inventoryModel)

                db.session.add(inventoryModel)
                db.session.commit()

                flash('Se ha agregado correctamente', 'completed')
                print('ye')
                return redirect(url_for('inventoryViews.inventory'))

        except Exception as e:
            flash('No se ha podido completar', 'error')
            print(e)
            return redirect(url_for('inventoryViews.inventory_create_processed_coffee'))
        

    return render_template('inventory/processed/inventoryCreateProcessedCoffee.html',
        inventoryForm=inventoryF,
        processedCoffeeForm=processedCoffeeF)


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

        inventoryParchmentToModify = Inventory.query.filter_by(product_id=processed.dry_parchment_coffee_id, category_id=1).first()
        inventoryParchmentToModify.quantity = inventoryParchmentToModify.quantity + processed.processed_parchment_weight

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

                inventoryModel = Inventory()
                inventoryF.populate_obj(inventoryModel)

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


