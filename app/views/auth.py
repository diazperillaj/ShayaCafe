from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app import bcrypt, login_manager
from app.models.user import User
from app.forms.login import loginForm

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET'])
def login_page():
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def login():

    userTemp = User.query.filter_by(username='Juan').first()
    login_user(userTemp)
    return redirect(url_for('index.home'))

    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('index.home'))
        else:
            flash('Error al inciar sesion, por favor valide sus credenciales', 'error')
            return render_template('loginForm.html', form=form) 
    return render_template('loginForm.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


