from flask import Blueprint, render_template, redirect, url_for, request
from app.forms.inventory import *
from app.models.inventory import *
from app.models.farmer import Farmer

inventoryViews = Blueprint('inventoryViews', __name__)



@inventoryViews.route('/')
def inventory():
    return render_template('inventory.html')



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

    return render_template('inventoryCreateCategory.html', form=form)



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
                variety = dryParchmentCoffeeF.variety.data,
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

        except Exception as e:
            print(f'Error\n{e}')
            #return redirect(url_for('inventoryViews.inventory'))

    return render_template('inventoryCreateDryParchmentCoffee.html',
                        inventoryForm=inventoryF,
                        dryParchmentCoffeeForm=dryParchmentCoffeeF)



@inventoryViews.route('/create/processed-coffee', methods=['GET','POST'])
def inventory_create_processed_coffee():

    inventoryF = inventoryForm()
    processedCoffeeF = processedCoffeeForm()

    """
    Pendiente por revisar (dry_parchment_coffee.id, dry_parchment_coffee.farmer_id.name)
    """
    processedCoffeeF.dry_parchment_coffee_id.choices = [
                        (dry_parchment_coffee.id, dry_parchment_coffee.farmer_id.name)
                        for dry_parchment_coffee in dryParchmentCoffee.query.all()
                        ]

    return render_template('inventoryCreateProcessedCoffee.html',
                        inventoryForm=inventoryF,
                        processedCoffeeForm=processedCoffeeF)



@inventoryViews.route('/create/others-in-inventory', methods=['GET','POST'])
def inventory_create_others_in_inventory():

    inventoryF = inventoryForm()
    othersInInventoryF = othersInInventoryForm()

    return render_template('inventoryCreateOthers.html',
                        inventoryForm=inventoryF,
                        othersInInventoryForm=othersInInventoryF)