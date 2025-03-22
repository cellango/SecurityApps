import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from models.team import Team
from models.application import Application, ApplicationType
from datetime import datetime, timedelta
import random

def seed_data():
    app = create_app()
    with app.app_context():
        # Create teams
        teams = [
            Team(name="Security Team", description="Team responsible for security oversight"),
            Team(name="Development Team", description="Main development team"),
            Team(name="Operations Team", description="Operations and infrastructure team"),
            Team(name="Compliance Team", description="Regulatory compliance team")
        ]
        
        for team in teams:
            db.session.add(team)
        db.session.commit()
        
        # Create applications
        current_time = datetime.utcnow()
        applications = [
            Application(
                name="Customer Portal",
                description="Main customer-facing web application",
                app_type=ApplicationType.BUILT,
                team_id=teams[1].id,
                security_score=92.5,
                catalog_id="APP-001",
                support_url="https://support.example.com/portal",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Internal Dashboard",
                description="Internal monitoring and analytics dashboard",
                app_type=ApplicationType.BUILT,
                team_id=teams[0].id,
                security_score=88.0,
                catalog_id="APP-002",
                support_url="https://wiki.internal/dashboard",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Payment Gateway",
                description="Third-party payment processing system",
                app_type=ApplicationType.BOUGHT,
                vendor_name="SecurePay Inc.",
                vendor_contact="support@securepay.example.com",
                team_id=teams[2].id,
                security_score=95.0,
                catalog_id="APP-003",
                support_url="https://securepay.example.com/support",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            ),
            Application(
                name="Authentication Service",
                description="Identity and access management service",
                app_type=ApplicationType.BUILT,
                team_id=teams[0].id,
                security_score=90.0,
                catalog_id="APP-004",
                support_url="https://wiki.internal/auth",
                last_scored=current_time - timedelta(days=random.randint(1, 10)),
                created_at=current_time,
                updated_at=current_time
            )
        ]
        
        for app in applications:
            db.session.add(app)
            db.session.commit()
        
        print("Data seeded successfully")
