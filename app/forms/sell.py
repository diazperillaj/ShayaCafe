from flask_wtf import FlaskForm
import datetime
from wtforms import StringField, IntegerField, SelectField, FloatField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired

class productForm(FlaskForm):
    name = StringField('Nombre producto', validators=[DataRequired()])
    price = FloatField('Precio individual', validators=[DataRequired()])
    submit = SubmitField('Agregar', render_kw={'class':'login-btn'})


class orderForm(FlaskForm):
    observation = StringField('Observacion')
    order_date = DateTimeLocalField('Fecha ingreso',
                            format='%Y-%m-%dT%H:%M',
                            default=datetime.datetime.now(),
                            validators=[DataRequired()])
    submit = SubmitField('Agregar', render_kw={'class':'login-btn'})

class orderDetailForm(FlaskForm):
    quantity = IntegerField('Cantidad', validators=[DataRequired()])
    product_id = SelectField('Producto', 
                            choices=[],
                            coerce=int,
                            validators=[DataRequired()])
    submit = SubmitField('Agregar', render_kw={'class':'login-btn'})