from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    history  = db.relationship('ChatHistory', backref='user', lazy=True)

class ChatHistory(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject     = db.Column(db.String(50))
    question    = db.Column(db.Text)
    explanation = db.Column(db.Text)
    quiz        = db.Column(db.Text)   # stored as JSON string
    topic       = db.Column(db.String(100))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)