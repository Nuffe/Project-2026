
from flask_login import UserMixin 


class User(UserMixin):
    def __init__(self, name, id, age, password):
        self.name = name
        self.id = id
        self.age = age
        self.password = password
    
    