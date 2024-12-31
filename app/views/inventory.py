from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms.inventory import *
from app.models.inventory import *
from app.models.farmer import Farmer
from sqlalchemy.orm import joinedload

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
                processed = False)
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


    return render_template('inventory/dry_parchment/inventoryEditDryParchmentCoffee.html',
        inventoryForm=inventoryF,
        dryParchmentCoffeeForm=dryParchmentF)



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

    if processedCoffeeF.validate_on_submit():

        try:
            processedModel = processedCoffee(
                dry_parchment_coffee_id = processedCoffeeF.dry_parchment_coffee_id.data,
                weight = processedCoffeeF.weight.data,
                processed_category = processedCoffeeF.processed_category.data.capitalize(),
                responsible = processedCoffeeF.responsible.data.capitalize(),
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

                db.session.commit()

                return redirect(url_for('inventoryViews.inventory'))
                

        except Exception as e:
            flash('Error, no se ha podido completar la actualizacion','error')
            print(e)

    return render_template('inventory/processed/inventoryEditProcessedCoffee.html',
        inventoryForm=inventoryF,
        processedCoffeeForm=processedCoffeeF)

@inventoryViews.route('/create/others-in-inventory', methods=['GET','POST'])
def inventory_create_others_in_inventory():

    inventoryF = inventoryForm()
    othersInInventoryF = othersInInventoryForm()

    if othersInInventoryF.validate_on_submit():
        try:

            othersInInventoryModel = othersInInventory(
                name = othersInInventoryF.name.data.capitalize(),
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