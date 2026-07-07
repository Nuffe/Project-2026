
from flask import Blueprint
from app.helpers import is_admin
from flask import render_template, flash
from flask import request
from db import get_users, get_all_users
from flask import request, redirect, url_for
from db import get_admins, get_users, delete_user, add_user
from werkzeug.security import generate_password_hash

import requests
from flask_login import current_user


bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route("/register")
@is_admin
def register():
    return render_template("register.html", users=get_users(), admins=get_admins())


@bp.route("/requestUsers")
def requesting():
    if request.headers["Key"] == "Admin":
        users = get_all_users()
        jsonUsers = []
        for user in users:
            jsonUser = {
                "name": user["name"],
                "age": user["age"],
                "role": user["role"],
                "id": user["ID"]
            }
            jsonUsers.append(jsonUser)
        return jsonUsers
    return {"error": "Missing permissions"} #Make this page or flask


@bp.route("/users", methods=["GET"])
@is_admin
def users():
    print("CURRENT USER ROLE", current_user.is_anonymous)
    if request.method == "GET":
        header = {"Key": "Admin"} #Place holder, make DB keys?
        response = requests.get("http://127.0.0.1:5000/admin/requestUsers", headers=header )
        if response:
            loadedResponse = response.json()
            return render_template("users.html", users=loadedResponse )
        else:
            print("RESPONSE FAILED")
    


@bp.route("/deleteUser", methods=["POST"])
@is_admin
def deleteUser():
    delete_user(request.form["name"])
    return redirect(url_for("admin.users"))

@bp.route("/addUser", methods=["POST"])
@is_admin
def addUser():
    if request.form["username"] and request.form["password"]:
        password = generate_password_hash(request.form["password"])
        add_user(request.form["username"], request.form["age"], password, request.form["role"])
        flash(f"User {request.form['username']} was successfully added")
    else:
        flash("Was unable to add user")
    return redirect(url_for("admin.register"))

