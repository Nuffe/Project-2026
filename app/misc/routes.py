
from flask import Blueprint
from app.helpers import is_admin
from flask import render_template
from flask import request
from db import get_users, get_all_users
import requests
from flask_login import current_user


bp = Blueprint('misc', __name__, url_prefix="/")

@bp.route("/hello")
def hello_world():
    display = "<p> WELL COME TO BLUE PRICE </p>"
    print("hello WORLD")
    return "<p> Hello world!</p>" + display


@bp.route("/home")
def home():
    print("hello HOME")
    return render_template("home.html")


@bp.route("/inside", methods=["POST", "GET"])
def inside():
    if request.method == "POST":
        return render_template("insideHome.html",  users = get_users())

    return render_template("InsideHome.html", users = get_users())


@bp.route("/requestUsers")
def users():
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
def requesting():
    print("CURRENT USER ROLE", current_user.is_anonymous)
    if request.method == "GET":
        header = {"Key": "Admin"} #Place holder, make DB keys?
        response = requests.get("http://127.0.0.1:5000/requestUsers", headers=header )
        if response:
            loadedResponse = response.json()
            return render_template("users.html", users=loadedResponse )
        else:
            print("RESPONSE FAILED")
