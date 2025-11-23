"""Visit model to track healthcare visits."""

import datetime
from src.config.database import db


class Visit(db.Model):
    """Record of a healthcare visit."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    cost = db.Column(db.Float, nullable=False, default=0.0)  # Cost charged (0 if within included visits)
    notes = db.Column(db.Text, nullable=True)  # Optional notes about the visit
    
    # Relationships
    user = db.relationship('User', backref='visits')
    subscription = db.relationship('Subscription', backref='visits')
