from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo

mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from .routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
