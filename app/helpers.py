from flask import redirect, url_for
from db import  query_db
from flask_login import current_user
from functools import wraps
from app.user import User



def is_admin(f):
    @wraps(f)
    def wrapFunction(*args, **kwargs):
        if current_user.is_anonymous:
            print("YOU ARE NOT LOGGED in")
            return redirect(url_for("misc.home"))
        query = "SELECT role FROM users WHERE ID = ?"
        result = query_db(query, (current_user.id,), one=True)
        if result["role"] == "Admin":
            print("you are admin, go ahead")
            return f(*args, **kwargs)
        else:
            print("You are not admin")
            return redirect(url_for("misc.home"))
    return wrapFunction

