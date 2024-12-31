from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired
import datetime

class inventoryForm(FlaskForm):
    product_id = IntegerField('Product ID')
    category_id = IntegerField('Category ID')
    quantity = IntegerField('Cantidad',
                            validators=[DataRequired()])
    entry_date = DateTimeLocalField('Fecha ingreso',
                            format='%Y-%m-%dT%H:%M',
                            default=datetime.datetime.now(),
                            validators=[DataRequired()])
    observation = StringField('Observaciones')
    submit = SubmitField('Agregar',
                            render_kw={"class": "login-btn"})

class categoryForm(FlaskForm):
    name = StringField('Nombre categoria',
                            validators=[DataRequired()])
    description = StringField('Descripcion')
    submit = SubmitField('Crear',
                            render_kw={"class": "login-btn"})

class dryParchmentCoffeeForm(FlaskForm):
    farmer_id = SelectField('Caficultor',
                            choices=[],
                            coerce=int,
                            validators=[DataRequired()])
    variety = StringField('Variedad',
                            validators=[DataRequired()])
    altitude = StringField('Altitud',
                            validators=[DataRequired()])
    submit = SubmitField('Agregar',
                            render_kw={"class": "login-btn"})

class processedCoffeeForm(FlaskForm):
    dry_parchment_coffee_id = SelectField('Pergamino seco',
                            choices=[],
                            coerce=int,
                            validators=[DataRequired()])
    weight = IntegerField('Tamaño individual',
                            validators=[DataRequired()])
    processed_category = StringField('Tipo molienda',
                            validators=[DataRequired()])
    responsible = StringField('Responsable',
                            validators=[DataRequired()])
    submit = SubmitField('Agregar',
                            render_kw={"class": "login-btn"})

class othersInInventoryForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired()])
    description = StringField('Descripcion')
    submit = SubmitField('Agregar',
                            render_kw={"class": "login-btn"})