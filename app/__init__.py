from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.auth.routes import bp as auth_bp
from app.misc.routes import bp as misc_bp
from app.admin.routes import bp as admin_bp
from db import close_connection
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
from app.tempFile import load_user #Is used by Flask, so needed here

csrf = CSRFProtect()
def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(misc_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    app.teardown_appcontext(close_connection)

    return app
