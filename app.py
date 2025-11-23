"""
Healthcare Subscription Management System

A Flask application for managing healthcare subscription plans.
Users can signup, login, view plans, and manage subscriptions.
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add project root to sys.path for 'src' module imports
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Load configuration from settings
    from src.config.settings import settings
    settings.ensure_data_dir()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET'] = settings.JWT_SECRET
    
    # Initialize database
    from src.config.database import db
    db.init_app(app)
    
    # Import models so they're registered with SQLAlchemy
    from src.models import User, Plan, Subscription, Visit
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Initialize default data using scripts
        from scripts.init_data import init_default_plans
        init_default_plans()
    
    # Register API blueprints
    from src.controllers.routes import register_blueprints
    register_blueprints(app)

    # Root route
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            'status': 'ok',
            'message': 'Healthcare Subscription API',
            'version': '2.0',
            'documentation': 'See README.md for full API documentation'
        })

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    from src.config.settings import settings
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
