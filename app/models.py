from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    clicks = db.Column(db.Integer, default=0)  # Число кликов пользователя

    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"
