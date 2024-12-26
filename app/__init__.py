from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from instance.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    from app.views.farmers import farmers
    from app.views.auth import auth
    from app.views.index import index
    from app.views.inventoryView import inventoryViews

    app.register_blueprint(inventoryViews, url_prefix='/Inventory')
    app.register_blueprint(farmers, url_prefix='/Farmers')
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app