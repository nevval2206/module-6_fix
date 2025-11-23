"""Application configuration settings."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Application Settings
        self.HOST = os.getenv('HOST', '0.0.0.0')
        self.PORT = int(os.getenv('PORT', 5001))
        self.DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'development')

        # Database - use absolute path
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / 'instance' / 'subscriptions.db'
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{db_path}')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        print(f"✓ Database URI: {self.SQLALCHEMY_DATABASE_URI}")

        # JWT Secret - MUST be set in production
        self.JWT_SECRET = os.getenv('JWT_SECRET')
        if not self.JWT_SECRET:
            # For development only - NEVER use in production
            self.JWT_SECRET = 'dev-secret-CHANGE-IN-PRODUCTION'
            if self.DEBUG:
                print("⚠️  WARNING: Using default JWT_SECRET. Set JWT_SECRET in .env file for production!")

    def ensure_data_dir(self):
        """Ensure instance directory exists for database."""
        import os
        project_root = Path(__file__).parent.parent.parent
        instance_dir = project_root / 'instance'
        instance_dir.mkdir(exist_ok=True)
        print(f"✓ Instance directory: {instance_dir}")


# Create singleton settings instance
settings = Settings()


# Legacy Config class for backward compatibility
class Config:
    """Base configuration (legacy support)."""
    settings_instance = settings
    
    PORT = settings.PORT
    DEBUG = settings.DEBUG
    SQLALCHEMY_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    JWT_SECRET = settings.JWT_SECRET
