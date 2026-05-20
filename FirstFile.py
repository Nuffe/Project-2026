from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template

app = Flask(__name__)


@app.route("/hello")
def hello_world():

    display = "<p> Is this message coming thought? </p>"
    return "<p> Hello world!</p>" + display

@app.route("/home")
@app.route("/home/<name>")
def home(name=None):
    return render_template("home.html", person=name)

@app.route("/variable/<username>")
def username(username):
    return f"User {escape(username)}"

@app.route("/about/")
def about():
    return "about page"

with app.test_request_context():
    print(url_for('home'))
    print(url_for('about'))
    print(url_for('username', username='Carl'))