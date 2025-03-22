import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.team import Team
from models.application import Application, ApplicationType
from models.risk_params import RiskParameters
from datetime import datetime, timedelta
import random

def check_if_seeded():
    """Check if database already has seed data"""
    with app.app_context():
        teams_count = Team.query.count()
        apps_count = Application.query.count()
        if teams_count > 0 or apps_count > 0:
            raise Exception("Database already contains data. Clear the database first if you want to reseed.")

def create_seed_data():
    """Create initial seed data for the application"""
    check_if_seeded()
    
    with app.app_context():
        print("Creating default risk parameters...")
        RiskParameters.get_default()

        print("Creating sample teams...")
        teams = [
            Team(
                name="Security Team",
                description="Team responsible for security oversight"
            ),
            Team(
                name="Development Team",
                description="Main development team"
            ),
            Team(
                name="Operations Team",
                description="Operations and infrastructure team"
            ),
            Team(
                name="Compliance Team",
                description="Regulatory compliance team"
            )
        ]
        
        for team in teams:
            db.session.add(team)
        db.session.commit()

        print("Creating sample applications...")
        current_time = datetime.utcnow()
        
        applications = [
            Application(
                name="Customer Portal",
                description="Main customer-facing web application",
                app_type=ApplicationType.INTERNAL,
                team_id=teams[1].id,  # Development Team
                catalog_id="APP-001",
                support_url="https://support.example.com/portal",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Internal Dashboard",
                description="Internal monitoring and analytics dashboard",
                app_type=ApplicationType.INTERNAL,
                team_id=teams[0].id,  # Security Team
                catalog_id="APP-002",
                support_url="https://wiki.internal/dashboard",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Payment Gateway",
                description="Third-party payment processing system",
                app_type=ApplicationType.VENDOR,
                vendor_name="SecurePay Inc.",
                vendor_contact="support@securepay.example.com",
                team_id=teams[2].id,  # Operations Team
                catalog_id="APP-003",
                support_url="https://securepay.example.com/support",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Authentication Service",
                description="Identity and access management service",
                app_type=ApplicationType.VENDOR,
                vendor_name="AuthCo",
                vendor_contact="support@authco.example.com",
                team_id=teams[0].id,  # Security Team
                catalog_id="APP-004",
                support_url="https://wiki.internal/auth",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            )
        ]
        
        for app in applications:
            db.session.add(app)
        
        # Commit all changes
        db.session.commit()
        print(f"Created {len(applications)} applications")

if __name__ == '__main__':
    create_seed_data()
