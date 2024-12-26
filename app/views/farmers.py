from flask import Blueprint, render_template, url_for, redirect
from app.forms.farmer import farmerForm
from app.models.farmer import Farmers
from app import db

farmers = Blueprint('farmers', __name__)

@farmers.route('/')
def farmer():
    farmers_list = Farmers.query.all()
    form = farmerForm()
    return render_template('farmers.html', farmers=farmers_list, form=form)

@farmers.route('/Create', methods=['GET','POST'])
def create_farmer():
    form=farmerForm()

    if form.validate_on_submit():
        farmer = Farmers(
            name = form.name.data.capitalize(),
            location = form.location.data.capitalize(),
            farm_name = form.farm_name.data.capitalize(),
            phone = form.phone.data,
            observation = form.observation.data if form.observation.data else "NA"
                        )
        db.session.add(farmer)
        db.session.commit()

        return redirect(url_for('farmers.farmer'))

    return render_template('farmersCreate.html', form=form)


@farmers.route('/Edit/<int:farmer_id>', methods=['POST'])
def edit_farmer(farmer_id: int):

    farmer = Farmers.query.get(farmer_id)
    if not farmer:
        return redirect(url_for('farmers.farmer'))
    
    form=farmerForm(obj=farmer)
          
    if form.validate_on_submit():
        farmer.name = form.name.data
        farmer.location = form.location.data
        farmer.farm_name = form.farm_name.data
        farmer.phone = form.phone.data
        farmer.observation = form.observation.data

        db.session.commit()

        return redirect(url_for('farmers.farmer'))
    
    form.submit.label.text = 'Editar'

    return render_template('farmersEdit.html', form=form)

@farmers.route('/Delete/<int:farmer_id>', methods=['POST'])
def delete_farmer(farmer_id: int):

    farmer = Farmers.query.get(farmer_id)
    if not farmer:
        return redirect(url_for('farmers.farmer'))

    db.session.delete(farmer)
    db.session.commit()

    return redirect(url_for('farmers.farmer'))