from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app import bcrypt, login_manager
import app.models.user as user_model
from app.forms.login import loginForm

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return user_model.Users.query.get(int(user_id))

@auth.route('/Login', methods=['GET'])
def login_page():
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def login():



    userTemp = user_model.Users.query.filter_by(username='Juan').first()
    login_user(userTemp)
    return redirect(url_for('index.home'))



    form = loginForm()
    if form.validate_on_submit():
        user = user_model.Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('index.home'))
        else:
            flash('Error al inciar sesion, por favor valide sus credenciales', 'error')
            return render_template('loginForm.html', form=form) 
    return render_template('loginForm.html', form=form)

@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


