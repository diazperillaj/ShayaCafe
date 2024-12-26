from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class farmerForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=20)])
    location = StringField('Ubicacion', validators=[DataRequired(), Length(min=2, max=120)])
    farm_name = StringField('Finca', validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField('Telefono', validators=[DataRequired(), Length(min=2, max=20)])
    observation = StringField('Observaciones')
    submit = SubmitField('Crear', render_kw={"class": "login-btn"})