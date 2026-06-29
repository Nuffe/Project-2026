from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from flask import request
from flask import g
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_users, delete_user, add_user

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"

guest_list = []

@app.route("/hello")
def hello_world():
    display = "<p> Is this message coming thought? </p>"
    return "<p> Hello world!</p>" + display


@app.route("/home")
@app.route("/home/<name>")
def home(name=None):
    return render_template("home.html", person=name)


@app.route("/home/inside", methods=["POST", "GET"])
def inside():
    users = get_users()
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
def deleteUser():
    delete_user(request.form["name"])
    return redirect(url_for("inside"))


@app.route("/addUser", methods=["POST"])
def addUser():
    add_user(request.form["username"],request.form["age"],request.form["password"])
    return redirect(url_for("inside"))






@app.route("/variable/<username>")
def username(username):
    return f"User {escape(username)}"

@app.route("/about/")
def about():
    return "about page"


@app.shell_context_processor
def make_shell_context():
    from db import get_db, query_db
    conn = get_db()
    return dict(conn=conn, cur=conn.cursor(), query_db=query_db)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()