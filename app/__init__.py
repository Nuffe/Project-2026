from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from flask import request
from flask import g
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_users, delete_user, add_user, query_db, get_admins, get_all_users
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from app.user import User
from functools import wraps
import requests
import json
from flask_wtf.csrf import CSRFProtect
from app.auth.routes import bp as auth_bp
from app.misc.routes import bp as misc_bp


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
from app.tempFile import load_user



#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = "static/uploads"

    load_dotenv()
    app.secret_key = os.getenv("SECRET_KEY")

    csrf = CSRFProtect(app)

    login_manager.init_app(app)

    guest_list = []

    app.register_blueprint(misc_bp)
    app.register_blueprint(auth_bp)


    return app
