import click
from flask.cli import with_appcontext
from app import db
from app.models.application import Application
from datetime import datetime

@click.command('seed-db')
@with_appcontext
def seed_db():
    """Seed the database with test data."""
    # Add test applications
    applications = [
        {
            'name': 'platform-web-graphic',
            'description': 'Web-based graphic design platform',
            'application_type': 'web',
            'department_name': 'Engineering',
            'team_name': 'Frontend',
            'owner_email': 'frontend@example.com'
        },
        {
            'name': 'backend-api-service',
            'description': 'Core backend API service',
            'application_type': 'api',
            'department_name': 'Engineering',
            'team_name': 'Backend',
            'owner_email': 'backend@example.com'
        },
        {
            'name': 'security-scanner',
            'description': 'Security vulnerability scanner',
            'application_type': 'service',
            'department_name': 'Security',
            'team_name': 'Security Ops',
            'owner_email': 'security@example.com'
        }
    ]

    for app_data in applications:
        app = Application(
            name=app_data['name'],
            description=app_data['description'],
            application_type=app_data['application_type'],
            department_name=app_data['department_name'],
            team_name=app_data['team_name'],
            owner_email=app_data['owner_email'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(app)

    try:
        db.session.commit()
        click.echo('Database seeded successfully!')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error seeding database: {str(e)}')
