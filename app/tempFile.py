from app import login_manager
from app.user import User
from db import query_db



@login_manager.user_loader
def load_user(user_id):
    print("LOAD_USER WAS RUN")
    result =  query_db("SELECT * FROM users WHERE ID = ?", (user_id,), one=True)
    if result is None:
        return None
    user = User(result["name"], result["ID"], result["age"], result["password"], result["role"])
    return user
