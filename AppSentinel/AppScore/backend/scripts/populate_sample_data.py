import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.team import Team
from models.application import Application, ApplicationType
from models.user import User
from models.score_history import ScoreHistory

def populate_sample_data():
    """Populate the database with sample data."""
    print("Clearing existing data...")
    
    # Clear existing data
    db.session.query(ScoreHistory).delete()
    db.session.query(Application).delete()
    db.session.query(Team).delete()
    db.session.query(User).delete()
    db.session.commit()
    
    print("Creating admin user...")
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        is_active=True
    )
    admin.set_password('admin123')  # Using admin123 as password
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user created successfully with password: admin123")

    print("Creating sample teams...")
    # Create teams
    teams = [
        Team(name="Security Team", description="Core security team"),
        Team(name="Development Team", description="Main development team"),
        Team(name="Infrastructure Team", description="Infrastructure and operations"),
        Team(name="Product Team", description="Product management and design")
    ]
    for team in teams:
        db.session.add(team)

    print("Creating sample applications...")
    # Create applications
    applications = [
        Application(
            name="Customer Portal",
            description="Main customer-facing web application",
            app_type=ApplicationType.WEB,
            catalog_id="APP001",
            support_url="https://support.example.com/portal",
            vendor_name="Internal",
            vendor_contact="support@internal.com",
            team=teams[1]  # Development Team
        ),
        Application(
            name="Admin Dashboard",
            description="Internal administration dashboard",
            app_type=ApplicationType.WEB,
            catalog_id="APP002",
            support_url="https://support.example.com/admin",
            vendor_name="Internal",
            vendor_contact="support@internal.com",
            team=teams[0]  # Security Team
        ),
        Application(
            name="Mobile App",
            description="Customer mobile application",
            app_type=ApplicationType.MOBILE,
            catalog_id="APP003",
            support_url="https://support.example.com/mobile",
            vendor_name="Internal",
            vendor_contact="mobile@internal.com",
            team=teams[1]  # Development Team
        )
    ]
    for app in applications:
        db.session.add(app)

    # Commit to get IDs
    db.session.commit()

    print("Creating score history...")
    # Create score history for each application
    now = datetime.utcnow()
    for app in applications:
        # Create 30 days of score history
        for days_ago in range(30):
            date = now - timedelta(days=days_ago)
            
            # Generate random scores that trend upward
            base_score = 50 + (days_ago * 1.5)  # Score improves over time
            variation = random.uniform(-5, 5)  # Add some random variation
            raw_score = min(100, max(0, base_score + variation))  # Ensure score is between 0 and 100
            score = round(raw_score)  # Round to nearest integer
            
            # Create score history entry
            score_history = ScoreHistory(
                application_id=app.id,
                score=score,
                rules_score=round(score * 0.7),  # 70% of total score, rounded
                ml_score=round(score * 0.3),     # 30% of total score, rounded
                details={
                    "findings": {
                        "critical": random.randint(0, 2),
                        "high": random.randint(1, 5),
                        "medium": random.randint(3, 8),
                        "low": random.randint(5, 15)
                    },
                    "improvements": [
                        "Updated security headers",
                        "Fixed SQL injection vulnerabilities",
                        "Implemented rate limiting"
                    ]
                },
                created_at=date
            )
            db.session.add(score_history)
            
            # Update application's last_scored
            if days_ago == 0:  # Most recent score
                app.last_scored = date

    # Commit all changes
    db.session.commit()
    print("Sample data created successfully!")

if __name__ == "__main__":
    with app.app_context():
        populate_sample_data()
