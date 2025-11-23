"""Plan model."""

import json
from src.config.database import db


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
