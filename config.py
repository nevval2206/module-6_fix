"""Configuration for Flask application."""

import os


class Config:
    """Base configuration."""

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///subscriptions.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret - MUST be set in production
    JWT_SECRET = os.environ.get('JWT_SECRET')
    if not JWT_SECRET:
        # For development only - NEVER use in production
        JWT_SECRET = 'dev-secret-CHANGE-IN-PRODUCTION'
        print("WARNING: Using default JWT_SECRET. Set JWT_SECRET environment variable for production!")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


# Default config
config = DevelopmentConfig
