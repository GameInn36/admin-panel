from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password, bio, file_extension):
        self.username = username
        self.password = password
        self.bio = bio
        self.file_extension = file_extension
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active
        
def get_user(user_id):
    db = current_app.config["db"]
    user = db.get_user(user_id)
    #password = current_app.config["PASSWORDS"].get(user_id)
    #user = db.get_user(user_id) if user.password else None
    if user is not None:
        user.is_admin = user.username in current_app.config["ADMIN_USERS"]
    return user