from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db, bcrypt, login_manager
from app.models import Users
from .forms import loginForm

auth = Blueprint('auth', __name__)

# @auth.before_request
# def before_request():
#     if not current_user.is_authenticated and request.endpoint not in ['auth.login', 'static', 'auth.register']:
#         return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@auth.route('/login', methods=['GET'])
def login_page():
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                # user.permanent = True
                # if 'next_url' in session:
                #     next = session.pop('next_url')
                #     return redirect(next)

                return redirect(url_for('views.home'))
        else:
            flash('Error al inciar sesion, por favor valide sus credenciales', 'error')
            return render_template('loginForm.html', form=form) 
    return render_template('loginForm.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


