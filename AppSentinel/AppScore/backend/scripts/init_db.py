import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def create_database():
    """Create the database if it doesn't exist"""
    try:
        conn = psycopg2.connect(
            host="postgres",  # Use the service name from docker-compose
            user="postgres",
            password="postgres",
            port=5432
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname='security_score_card'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute('CREATE DATABASE security_score_card')
            print("Database created successfully")
        else:
            print("Database already exists")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

def init_db():
    """Initialize the database tables"""
    try:
        app = create_app()
        with app.app_context():
            # Drop all tables and recreate them
            db.drop_all()
            db.create_all()
            print("Database tables created successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    create_database()
    init_db()
