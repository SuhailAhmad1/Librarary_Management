from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(180))
    email = db.Column(db.String(100))
    password = db.Column(db.String(256))
    role = db.Column(db.String(100))

    def __init__(self, email, password):
        self.username = ""
        self.email = email
        self.password = password
        self.role = "user"