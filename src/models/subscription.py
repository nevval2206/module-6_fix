"""Subscription model."""

import datetime
from src.config.database import db


class Subscription(db.Model):
    """User subscription model."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    def get_visits_count(self):
        """Get total number of visits used in this subscription."""
        from src.models.visit import Visit
        return Visit.query.filter_by(subscription_id=self.id).count()
    
    def get_visits_this_month(self):
        """Get number of visits used in the current month."""
        from src.models.visit import Visit
        now = datetime.datetime.utcnow()
        start_of_month = datetime.datetime(now.year, now.month, 1)
        return Visit.query.filter(
            Visit.subscription_id == self.id,
            Visit.visit_date >= start_of_month
        ).count()
    
    def calculate_visit_cost(self):
        """Calculate the cost for a new visit based on plan limits."""
        from src.models.plan import Plan
        plan = Plan.query.get(self.plan_id)
        if not plan:
            return 0
        
        # Check if plan has unlimited visits
        if plan.included_visits == float('inf'):
            return 0
        
        # Count visits used this month
        visits_this_month = self.get_visits_this_month()
        
        # If within included visits, no charge
        if visits_this_month < plan.included_visits:
            return 0
        
        # Extra visit - charge the extra visit price
        return plan.extra_visit_price
