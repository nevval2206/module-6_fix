"""Initialize default subscription plans in the database."""

import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import db
from src.models import Plan


def init_default_plans():
    """Initialize default subscription plans if they don't exist."""
    if Plan.query.count() == 0:
        plans = [
            {
                'name': 'Lite Care Pack',
                'price': 25,
                'included_visits': 2,
                'extra_visit_price': 15,
                'services': ['Basic check-up']
            },
            {
                'name': 'Standard Health Pack',
                'price': 45,
                'included_visits': 4,
                'extra_visit_price': 20,
                'services': ['Check-up', 'Blood analysis']
            },
            {
                'name': 'Chronic Care Pack',
                'price': 80,
                'included_visits': 8,
                'extra_visit_price': 18,
                'services': ['Blood tests', 'X-ray', 'ECG']
            },
            {
                'name': 'Unlimited Premium Pack',
                'price': 120,
                'included_visits': float('inf'),
                'extra_visit_price': 0,
                'services': ['All diagnostics', 'X-ray', 'Ultrasound']
            }
        ]

        for p in plans:
            plan = Plan(
                name=p['name'],
                price=p['price'],
                included_visits=p['included_visits'],
                extra_visit_price=p['extra_visit_price'],
                services_json=json.dumps(p['services'])
            )
            db.session.add(plan)

        db.session.commit()
        print(f"✓ Initialized {len(plans)} default subscription plans")
    else:
        print(f"✓ Plans already exist ({Plan.query.count()} plans found)")


if __name__ == '__main__':
    """Run this script directly to initialize data."""
    from app import create_app
    
    app = create_app()
    with app.app_context():
        init_default_plans()
