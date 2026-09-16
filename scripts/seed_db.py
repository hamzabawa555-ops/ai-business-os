"""Database Seeding Script"""

import logging
from backend.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """
    Seed database with initial data
    """
    db = SessionLocal()
    
    try:
        logger.info("Starting database seeding...")
        
        # TODO: Add seed data here
        # Example:
        # - Create default users
        # - Create default roles
        # - Create example workflows
        # - Create sample data
        
        logger.info("Database seeding completed successfully")
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
