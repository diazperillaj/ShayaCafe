from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class inventoryForm(FlaskForm):
    product_id = SelectField('')

class categoryForm(FlaskForm):
    name = StringField('Nombre categoria',
                            validators=[DataRequired()])
    description = StringField('Descripcion',
                            validators=[DataRequired()])
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