import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length


class loginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])    
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Login', render_kw={"class": "login-btn"})

class productForm(FlaskForm):
    product = SelectField('Producto',
                            choices=[],
                            coerce=int,
                            validators=[DataRequired(), Length(min=2, max=200)])
    category = SelectField('Categoria',
                            choices=[],
                            coerce=int,
                            validators=[DataRequired(), Length(min=2, max=200)])
    quantity = StringField('Cantidad',
                            validators=[DataRequired(), Length(min=1, max=200)])
    price = StringField('Precio',
                            validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Agregar', render_kw={"class": "login-btn"})

class salesForm(FlaskForm):
    name = StringField('Producto',
                            validators=[DataRequired(), Length(min=2, max=200)])
    category = StringField('Categoria',
                            validators=[DataRequired(), Length(min=2, max=200)])
    quantity = StringField('Cantidad',
                            validators=[DataRequired(), Length(min=1, max=200)])
    price = StringField('Precio',
                            validators=[DataRequired(), Length(min=1, max=200)])
    date = DateTimeLocalField('Fecha',
                            format='%Y-%m-%dT%H:%M',
                            default=datetime.datetime.now(),
                            validators=[DataRequired()])
    submit = SubmitField('Agregar', render_kw={"class": "login-btn"})
