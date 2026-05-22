from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import Flask, flash, request, redirect, url_for
from flask import request
from werkzeug.utils import secure_filename
import os

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
def inside(guest = None):
    if request.method == "POST":

        guest_list.append(request.form["name"])
        print("PEOPLE: ", guest_list)
        return render_template("insideHome.html", guests = guest_list)

    return render_template("InsideHome.html", guests = guest_list)

@app.route("/variable/<username>")
def username(username):
    return f"User {escape(username)}"

@app.route("/about/")
def about():
    return "about page"

@app.route("/clearGuestList", methods=["POST"])
def clear():
    guest_list.clear()
    return redirect(url_for("inside"))

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