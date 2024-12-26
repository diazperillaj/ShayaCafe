from flask import Blueprint, render_template

inventoryViews = Blueprint('inventoryViews', __name__)

@inventoryViews.route('/')
def inventory():
    return render_template('inventory.html')