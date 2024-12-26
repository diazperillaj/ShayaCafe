from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

index = Blueprint('index', __name__)

@index.route('/home')
@login_required
def home():
    return render_template('index.html')