
from flask import Blueprint
from app.helpers import is_admin
from flask import render_template
from flask import request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from app.user import User
from flask import Flask, flash, request, redirect, url_for
from db import query_db, get_admins, get_users
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("misc.inside"))

    if  request.method == "POST":
        username= request.form["username"]
        password = request.form["password"]

        query = "SELECT * FROM users WHERE name = ?"
        result = query_db(query, (username,), one=True)
        print("TRYING TO LOG IN")
        if result:
            passwordCheck = check_password_hash(result["password"], password)
        else:
            passwordCheck = None

        if passwordCheck:
            user = User(result["name"], result["ID"], result["age"], result["password"], result["role"]  )
            login = login_user(user)
            if login:
                print("login success")
            else:
                print("login fail")
            return redirect(url_for("misc.inside"))
        
        print("Wong password")
        return redirect(url_for("auth.login"))   
    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    print(current_user.name)
    print(current_user.get_id())
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route("/register")
@is_admin
def register():
    return render_template("register.html", users=get_users(), admins=get_admins())




