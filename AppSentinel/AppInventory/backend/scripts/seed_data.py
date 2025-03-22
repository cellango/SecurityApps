"""
Script to seed the database with sample data.
Can be run directly or invoked via an endpoint.
"""
from app import create_app, db
from app.models.application import Application
from app.models.department import Department
from app.models.team import Team
from app.models.user import User
from datetime import datetime, timedelta, date
import random

def generate_test_score():
    return round(random.uniform(65.0, 98.0), 1)

def generate_random_date(start_year=2024):
    start = date(start_year, 1, 1)
    days = random.randint(0, 365)
    return start + timedelta(days=days)

def get_or_create(session, model, **kwargs):
    """Get an existing record or create it if it doesn't exist"""
    filters = {k: v for k, v in kwargs.items() if k != 'defaults'}
    instance = session.query(model).filter_by(**filters).first()
    if instance:
        return instance, False
    else:
        if 'defaults' in kwargs:
            kwargs.update(kwargs.pop('defaults'))
        instance = model(**kwargs)
        session.add(instance)
        return instance, True

def seed_data():
    """Seed the database with initial data"""
    app = create_app()
    
    with app.app_context():
        print("Starting database seeding...")
        
        # Create admin user if doesn't exist
        admin_user, created = get_or_create(
            db.session,
            User,
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin',
                'first_name': 'System',
                'last_name': 'Administrator'
            }
        )
        if created:
            print("Created admin user")
        
        # Create departments
        departments_data = [
            {
                'name': 'Engineering',
                'description': 'Software Engineering Department',
                'teams': [
                    {'name': 'Backend Team', 'description': 'Backend Development Team'},
                    {'name': 'Frontend Team', 'description': 'Frontend Development Team'},
                    {'name': 'DevOps Team', 'description': 'Infrastructure and Operations Team'},
                    {'name': 'Security Team', 'description': 'Application Security Team'}
                ]
            },
            {
                'name': 'Finance',
                'description': 'Finance and Accounting Department',
                'teams': [
                    {'name': 'Accounting Team', 'description': 'Financial Accounting Team'},
                    {'name': 'Treasury Team', 'description': 'Treasury Management Team'}
                ]
            },
            {
                'name': 'Sales',
                'description': 'Sales and Business Development',
                'teams': [
                    {'name': 'Direct Sales', 'description': 'Direct Sales Team'},
                    {'name': 'Channel Sales', 'description': 'Partner and Channel Sales'},
                    {'name': 'Sales Operations', 'description': 'Sales Support and Operations'}
                ]
            },
            {
                'name': 'Marketing',
                'description': 'Marketing and Communications',
                'teams': [
                    {'name': 'Digital Marketing', 'description': 'Digital Marketing Team'},
                    {'name': 'Content Team', 'description': 'Content Creation Team'},
                    {'name': 'Brand Team', 'description': 'Brand Management Team'}
                ]
            },
            {
                'name': 'HR',
                'description': 'Human Resources',
                'teams': [
                    {'name': 'Recruitment', 'description': 'Talent Acquisition Team'},
                    {'name': 'HR Operations', 'description': 'HR Operations Team'}
                ]
            }
        ]
        
        departments = {}
        teams = {}
        
        # Create departments and teams
        for dept_data in departments_data:
            dept, created = get_or_create(
                db.session,
                Department,
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            if created:
                print(f"Created {dept.name} department")
            departments[dept.name] = dept
            
            # Commit department before creating teams
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error creating department: {str(e)}")
                return
            
            # Create teams for this department
            for team_data in dept_data['teams']:
                team, created = get_or_create(
                    db.session,
                    Team,
                    name=team_data['name'],
                    department_id=dept.id,
                    defaults={'description': team_data['description']}
                )
                if created:
                    print(f"Created {team.name} team")
                teams[team.name] = team
                
                # Commit each team
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error creating team: {str(e)}")
                    return
        
        try:
            db.session.commit()
            print("Successfully created departments and teams")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating departments and teams: {str(e)}")
            return
        
        # Application creation helpers
        service_prefixes = ['Auth', 'User', 'Payment', 'Order', 'Inventory', 'Notification', 'Analytics', 'Search', 'Cache', 'Queue']
        service_suffixes = ['Service', 'API', 'Manager', 'Handler', 'Processor', 'Engine', 'System', 'Gateway']
        auth_methods = ['JWT', 'OAuth2', 'SAML', 'Basic Auth', 'API Key']
        vendors = ['Internal', 'AWS', 'Google Cloud', 'Azure', 'DataDog', 'Elastic', None]
        
        # Application templates for each department
        application_templates = {
            'Engineering': {
                'prefixes': ['api-', 'service-', 'app-', 'tool-', 'platform-'],
                'suffixes': ['-backend', '-frontend', '-core', '-infra', '-monitoring'],
                'types': ['service', 'web', 'platform'],
                'min_apps': 40
            },
            'Finance': {
                'prefixes': ['finance-', 'accounting-', 'billing-', 'payment-'],
                'suffixes': ['-system', '-service', '-app', '-platform'],
                'types': ['service', 'web', 'platform'],
                'min_apps': 20
            },
            'Sales': {
                'prefixes': ['sales-', 'crm-', 'lead-', 'opportunity-'],
                'suffixes': ['-tracker', '-analytics', '-dashboard', '-system'],
                'types': ['service', 'web'],
                'min_apps': 15
            },
            'Marketing': {
                'prefixes': ['marketing-', 'campaign-', 'analytics-', 'content-'],
                'suffixes': ['-platform', '-dashboard', '-system', '-tool'],
                'types': ['service', 'web'],
                'min_apps': 15
            },
            'HR': {
                'prefixes': ['hr-', 'recruiting-', 'employee-', 'training-'],
                'suffixes': ['-system', '-portal', '-platform', '-app'],
                'types': ['service', 'web'],
                'min_apps': 10
            }
        }

        # Create applications for each department
        total_apps = 0
        for dept_name, dept in departments.items():
            dept_teams = [team for team in teams.values() if team.department_id == dept.id]
            template = application_templates[dept_name]
            num_apps = max(template['min_apps'], random.randint(template['min_apps'], template['min_apps'] + 10))
            
            print(f"\nCreating {num_apps} applications for {dept_name}...")
            
            for i in range(num_apps):
                team = random.choice(dept_teams)
                app_type = random.choice(template['types'])
                
                if app_type == 'service':
                    name = f"{random.choice(template['prefixes'])}{random.choice(template['suffixes'])}-{i+1}"
                else:
                    name = f"{random.choice(template['prefixes'])}{app_type}-{i+1}"

                deployment_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
                app, created = get_or_create(
                    db.session,
                    Application,
                    name=name,
                    defaults={
                        'description': f'A {app_type} application for {dept_name}',
                        'team_id': team.id,
                        'team_name': team.name,
                        'department_name': dept_name,
                        'owner_id': f'user{i}',
                        'owner_email': f'user{i}@example.com',
                        'test_score': random.uniform(0, 100),
                        'test_score_date': datetime.utcnow() - timedelta(days=random.randint(0, 90)),
                        'last_security_review': datetime.utcnow() - timedelta(days=random.randint(0, 180)),
                        'next_security_review': datetime.utcnow() + timedelta(days=random.randint(30, 180)),
                        'deployment_date': deployment_date,
                        'last_update_date': deployment_date + timedelta(days=random.randint(0, 180)),
                        'vendor_name': random.choice(vendors),
                        'vendor_contact': 'support@vendor.com' if random.choice(vendors) else None,
                        'contract_expiration': datetime.utcnow() + timedelta(days=random.randint(30, 365)) if random.choice(vendors) else None,
                        'data_classification': random.choice(['Public', 'Internal', 'Confidential', 'Restricted']),
                        'authentication_method': random.choice(auth_methods),
                        'requires_2fa': random.choice([True, False]),
                        'application_type': app_type
                    }
                )
                if created:
                    total_apps += 1
                    print(f"Created application {total_apps}: {app.name} for {team.name}")
                
                # Commit every 10 applications
                if total_apps % 10 == 0:
                    try:
                        db.session.commit()
                        print(f"Committed batch of applications (total: {total_apps})")
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error creating applications batch: {str(e)}")
                        return

        try:
            db.session.commit()
            print(f"\nSuccessfully created all applications (total: {total_apps})")
        except Exception as e:
            db.session.rollback()
            print(f"Error in final commit: {str(e)}")
            return

if __name__ == '__main__':
    seed_data()
