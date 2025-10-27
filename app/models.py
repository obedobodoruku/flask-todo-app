from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(21), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.todo}', '{self.date_posted}')"
