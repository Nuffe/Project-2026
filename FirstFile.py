from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/hello")
def hello_world():

    display = "<p> Is this message coming thought? </p>"
    return "<p> Hello world!</p>" + display

@app.route("/home")
def home():
    message = "<p> This is the home page ;) </p>"
    return message

@app.route("/variable/<username>")
def username(username):
    return f"User {escape(username)}"

@app.route("/about/")
def about():
    return "about page"