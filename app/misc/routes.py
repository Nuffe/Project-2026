
from flask import Blueprint
from flask import render_template
from db import get_users
from flask import  request
from db import get_users

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



# Future idea, look into dynamic return template, so route can be used elsewhere
''' REDO, TO WORK WITH BLUEPRINTS
@bp.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return render_template("InsideHome.html", guest=guest_list, error="badFile")
    file = request.files['file']
    if file.filename.endswith((".jpg", ".png", ".gif")):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template("InsideHome.html", guest=guest_list, image=file.filename)
    else:
         return render_template("InsideHome.html", guest=guest_list, error="noImage")
'''