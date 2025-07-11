from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class loginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])    
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Login', render_kw={"class": "login-btn"})
