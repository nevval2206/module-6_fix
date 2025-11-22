"""
Healthcare Subscription Management System

A Flask application for managing healthcare subscription plans.
Users can signup, login, view plans, and manage subscriptions.
"""

from flask import Flask, jsonify
import json

from config import config
from models import db, Plan
from auth import auth_bp
from routes import plans_bp


def create_app(config_object=config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plans_bp, url_prefix='/api')

    # Create tables and initialize data
    with app.app_context():
        db.create_all()
        init_default_plans()

    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Healthcare Subscription API',
            'endpoints': {
                'auth': {
                    'signup': 'POST /api/auth/signup',
                    'login': 'POST /api/auth/login',
                    'logout': 'POST /api/auth/logout',
                    'me': 'GET /api/auth/me'
                },
                'plans': {
                    'list': 'GET /api/plans',
                    'subscriptions': 'GET /api/subscriptions',
                    'subscribe': 'POST /api/subscriptions',
                    'cancel': 'DELETE /api/subscriptions/<id>'
                }
            }
        })

    return app


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


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
