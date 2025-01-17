from flask import Blueprint, render_template, url_for, redirect, flash, make_response
from app.forms.farmer import farmerForm
from app.models.farmer import Farmer
from app import db
from weasyprint import HTML
import os


farmers = Blueprint('farmers', __name__)

@farmers.route('/')
def farmer():
    farmers_list = Farmer.query.all()
    form = farmerForm()
    return render_template('farmer/farmers.html', farmers=farmers_list, form=form)

@farmers.route('/create', methods=['GET','POST'])
def create_farmer():
    try:
        form=farmerForm()

        if form.validate_on_submit():
            farmer = Farmer(
                name = form.name.data.title(),
                location = form.location.data.title(),
                farm_name = form.farm_name.data.title(),
                phone = form.phone.data,
                observation = form.observation.data if form.observation.data else "NA"
                            )
            db.session.add(farmer)
            db.session.commit()

            return redirect(url_for('farmers.farmer'))
    except Exception as e:
        flash('No se ha podido crear el caficultor, por favor mirar consola para descripcion del error','error')
        print(e)

    return render_template('farmer/farmersCreate.html', form=form)


@farmers.route('/edit/<int:farmer_id>', methods=['POST'])
def edit_farmer(farmer_id: int):

    try:
        farmer = Farmer.query.get(farmer_id)
        if not farmer:
            return redirect(url_for('farmers.farmer'))
        
        form=farmerForm(obj=farmer)
        if form.validate_on_submit():
            form.farm_name.data = form.farm_name.data.capitalize()
            form.name.data = form.name.data.title()
            form.location.data = form.location.data.title()
            form.populate_obj(farmer)

            db.session.commit()

            return redirect(url_for('farmers.farmer'))
        
    except Exception as e:
        flash('No se ha podido editar, por favor mirar consola para descripcion del error','error')
        print(e)

    return render_template('farmer/farmersEdit.html', form=form)

@farmers.route('/delete/<int:farmer_id>', methods=['POST'])
def delete_farmer(farmer_id: int):

    try:
        farmer = Farmer.query.get(farmer_id)
        if not farmer:
            return redirect(url_for('farmers.farmer'))

        db.session.delete(farmer)
        db.session.commit()
    except Exception as e:
        flash('No se ha podido eliminar el caficultor, por favor verifique que no tiene cafes relacionados','error')
        print(e)
    return redirect(url_for('farmers.farmer'))




