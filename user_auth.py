from flask_login import UserMixin

# Simple in-memory user store (can be replaced with a database later)
users = {
    'admin': {'password': 'admin123'},
    'user1': {'password': 'password1'}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def authenticate(username, password):
    if username in users and users[username]['password'] == password:
        return User(username)
    return None
