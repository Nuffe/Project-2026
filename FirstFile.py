from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
from flask import redirect
from flask import request

app = Flask(__name__)

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
