"""Database models for healthcare subscription system."""

import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User account model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)  # bcrypt hashed

    subscriptions = db.relationship('Subscription', backref='user', lazy=True)


class Plan(db.Model):
    """Subscription plan model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    included_visits = db.Column(db.Float, nullable=False)  # numeric or inf
    extra_visit_price = db.Column(db.Float, nullable=False)
    services_json = db.Column(db.Text, nullable=False)

    subscriptions = db.relationship('Subscription', backref='plan', lazy=True)

    def services(self):
        """Parse and return services as list."""
        return json.loads(self.services_json)


class Subscription(db.Model):
    """User subscription model."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
