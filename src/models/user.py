"""User model."""

from src.config.database import db


class User(db.Model):
    """User account model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)  # bcrypt hashed

    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
