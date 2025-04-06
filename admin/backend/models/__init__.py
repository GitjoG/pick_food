from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the app"""
    db.init_app(app)
    
    # Import all models here
    from . import user, restaurant, recommendation, statistics, settings
    
    # Import all models to ensure they are registered with SQLAlchemy
    from .user import User
    from .restaurant import Restaurant
    from .admin import Admin
    
    with app.app_context():
        # Create all tables
        db.create_all() 