"""Register all application blueprints."""

from flask import Flask


def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application.
    
    Args:
        app: Flask application instance
    """
    from src.controllers.auth import auth_bp
    from src.controllers.plans import plans_bp
    from src.controllers.visits import visits_bp
    
    # Register authentication routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Register plans and subscriptions routes
    app.register_blueprint(plans_bp, url_prefix='/api')
    
    # Register visit tracking routes
    app.register_blueprint(visits_bp, url_prefix='/api')
    
    print("✓ Registered all blueprints")
