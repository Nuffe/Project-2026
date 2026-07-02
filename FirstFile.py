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
from user import User
from functools import wraps
import requests
import json


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)

guest_list = []

# Add Error page or popup instead of comments
def is_admin(f):
    @wraps(f)
    def wrapFunction(*args, **kwargs):
        if current_user.is_anonymous:
            print("YOU ARE NOT LOGGED in")
            return redirect(url_for("home"))
        query = "SELECT role FROM users WHERE ID = ?"
        result = query_db(query, (current_user.id,), one=True)
        if result["role"] == "Admin":
            print("you are admin, go ahead")
            return f(*args, **kwargs)
        else:
            print("You are not admin")
            return redirect(url_for("home"))
    return wrapFunction


@app.route("/requestUsers")
def users():
    if request.headers["Key"] == "Admin":
        users = get_all_users()
        jsonUsers = []
        print(request.headers)
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


@app.route("/users", methods=["GET"])
@is_admin
def requesting():
    if request.method == "GET":
        header = {"Key": "Admin"} #Place holder, make DB keys?
        response = requests.get("http://127.0.0.1:5000/requestUsers", headers=header )
        if response:
            loadedResponse = response.json()
            return render_template("users.html", users=loadedResponse )
        else:
            print("RESPONSE FAILED")

        
@app.route("/hello")
@is_admin
def hello_world():
    display = "<p> Is this message coming thought? </p>"
    print("hello WORLD")
    return "<p> Hello world!</p>" + display


@app.route("/home")
@app.route("/home/<name>")
def home(name=None):
    return render_template("home.html", person=name)


@app.route("/register")
@is_admin
def register():
    return render_template("register.html", users=get_users(), admins=get_admins())

@app.route("/home/inside", methods=["POST", "GET"])
def inside():
    if request.method == "POST":
        guest_list.append(request.form["name"])
        print("PEOPLE: ", guest_list)
        return render_template("insideHome.html", guests = guest_list, users = get_users())

    return render_template("InsideHome.html", guests = guest_list, users = get_users())


@app.route("/clearGuestList", methods=["POST"])
def clear():
    guest_list.clear()
    return redirect(url_for("inside"))


# Future idea, look into dynamic return template, so route can be used elsewhere
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return render_template("InsideHome.html", guest=guest_list, error="badFile")
    file = request.files['file']
    if file.filename.endswith((".jpg", ".png", ".gif")):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template("InsideHome.html", guest=guest_list, image=file.filename)
    else:
         return render_template("InsideHome.html", guest=guest_list, error="noImage")
    

@app.route("/deleteUser", methods=["POST"])
@is_admin
def deleteUser():
    delete_user(request.form["name"])
    return redirect(url_for("register"))


@app.route("/addUser", methods=["POST"])
@is_admin
def addUser():
    print(request.form["role"])
    if request.form["username"] and request.form["password"]:
        password = generate_password_hash(request.form["password"])
        add_user(request.form["username"],request.form["age"], password, request.form["role"])
    return redirect(url_for("register"))



@app.route("/variable/<username>")
def username(username):
    return f"User {escape(username)}"

@app.route("/about/")
def about():
    return "about page"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("inside"))

    if  request.method == "POST":
        username= request.form["username"]
        password = request.form["password"]

        query = "SELECT * FROM users WHERE name = ?"
        result = query_db(query, (username,), one=True)

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
            return redirect(url_for("inside"))
        
        print("Wong password")
        return redirect(url_for("login"))   
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    print(current_user.name)
    print(current_user.get_id())
    logout_user()
    return redirect(url_for("login"))

@app.shell_context_processor
def make_shell_context():
    from db import get_db, query_db, change_db
    conn = get_db()
    return dict(conn=conn, cur=conn.cursor(), query_db=query_db, change_db=change_db)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@login_manager.user_loader
def load_user(user_id):
    print("LOAD_USER WAS RUN")
    result =  query_db("SELECT * FROM users WHERE ID = ?", (user_id,), one=True)
    if result is None:
        return None
    user = User(result["name"], result["ID"], result["age"], result["password"], result["role"])
    return user




