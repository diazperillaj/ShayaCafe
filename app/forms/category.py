from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class categoryForm(FlaskForm):
    name = StringField('Nombre categoria', validators=[DataRequired()])
    description = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Crear', render_kw={"class": "login-btn"})