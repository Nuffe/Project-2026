
from flask_login import UserMixin 

#UserMixin = is_authenticated, is_active, is_anonymous and get_id()
class User(UserMixin):
    def __init__(self, name, id, age, password):
        self.name = name
        self.id = id
        self.age = age
        self.password = password
    
    