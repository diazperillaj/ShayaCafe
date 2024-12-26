from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class dryParchmentCoffeeForm(FlaskForm):
    farmer_id = SelectField('Caficultor',
                            choices=[],
                            coerce=int,
                            validators=[DataRequired()])
    variety = StringField('Variedad',
                            validators=[DataRequired()])
    altitude = StringField('Altitud',
                            validators=[DataRequired()])