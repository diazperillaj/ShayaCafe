from flask import Blueprint, render_template
from app.forms.category import categoryForm

inventoryViews = Blueprint('inventoryViews', __name__)

@inventoryViews.route('/')
def inventory():
    return render_template('inventory.html')

@inventoryViews.route('/create/category')
def inventory_create_category():
    form = categoryForm()
    return render_template('inventoryCreateCategory.html', form=form)


@inventoryViews.route('/create/dry-parchment-coffee')
def inventory_create_dry_parchment_coffee():
    form = categoryForm()
    return render_template('inventoryCreateCategory.html', form=form)