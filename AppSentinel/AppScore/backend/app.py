"""
Security Score Card - Main Application

A comprehensive security scoring and monitoring system for applications.

Authors:
    Clement Ellango
    Carolina Clement

Copyright (c) 2024. All rights reserved.
"""

from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from sqlalchemy import and_, func
from dotenv import load_dotenv
from extensions import db
from models.team import Team
from models.application import Application, ApplicationType
from models.user import User
from models.score_history import ScoreHistory
from models.finding import Finding
from models.risk_params import RiskParameters
from services.auth_service import AuthService
from services.report_service import ReportService
import logging
import os
import traceback
import jwt
import random
from datetime import timedelta
from config import get_config
from utils.logger import debug_log, log_info, log_debug, log_error
from utils.base_classes import BaseAPIEndpoint, BaseDataService
from utils.constants import MESSAGES, SCORE_RANGES
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app with configuration
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Set SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app,
     resources={
         r"/api/*": {
             "origins": ["http://localhost:3000", "http://localhost:3001"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Range", "X-Total-Count"],
             "supports_credentials": True,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         }
     })
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Initialize JWT
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Change this in production

# Initialize database

@app.before_request
@debug_log
def log_request_info():
    """Log request information in debug mode."""
    log_debug(f"Request Method: {request.method}")
    log_debug(f"Request URL: {request.url}")
    log_debug(f"Request Headers: {dict(request.headers)}")
    if request.is_json:
        log_debug(f"Request JSON: {request.get_json()}")

@app.after_request
@debug_log
def log_response_info(response):
    """Log response information in debug mode."""
    log_debug(f"Response Status: {response.status}")
    log_debug(f"Response Headers: {dict(response.headers)}")
    return response

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler with logging."""
    log_error(f"Unhandled error: {str(error)}", exc_info=True)
    return jsonify({"error": str(error)}), 500

def require_auth(f):
    """Decorator to require authentication for routes"""
    def wrapper(*args, **kwargs):
        # Always allow OPTIONS requests
        if request.method == 'OPTIONS':
            return '', 204

        app.logger.info(f"=== Auth Check for {request.path} ===")
        app.logger.info(f"Request headers: {dict(request.headers)}")
        
        auth_header = request.headers.get('Authorization')
        app.logger.info(f"Authorization header: {auth_header if auth_header else 'None'}")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            app.logger.warning("No token provided or invalid format")
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        app.logger.info("Token extracted from header")
        
        try:
            # Verify token
            verification_result = auth_service.verify_token(token)
            app.logger.info(f"Token verification result: {verification_result is not None}")
            app.logger.info(f"Token verification details: {verification_result}")
            
            if verification_result:
                app.logger.info("Token verification successful")
                return f(*args, **kwargs)
            else:
                app.logger.warning("Token verification failed")
                return jsonify({'error': 'Invalid token'}), 401
                
        except Exception as e:
            app.logger.error(f"Token verification error: {str(e)}")
            app.logger.error(f"Token verification error details: {e.__dict__}")
            return jsonify({'error': str(e)}), 401
    
    wrapper.__name__ = f.__name__
    return wrapper

# Load environment variables
load_dotenv()

# Initialize services
auth_service = AuthService(db.session, app.config['SECRET_KEY'])

# Create tables if they don't exist
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables checked/created successfully")
    except Exception as e:
        logger.error(f"Error checking/creating database tables: {str(e)}")

@app.before_first_request
def init_app():
    global auth_service
    if auth_service is None:
        auth_service = AuthService(session=db.session, secret_key=app.config['SECRET_KEY'])
    
    # Create admin user if it doesn't exist
    try:
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully")
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        db.session.rollback()

def get_application(app_id):
    """Get application by ID."""
    try:
        application = db.session.query(Application).get(app_id)
        if not application:
            return jsonify({"error": "Application not found"}), 404
        
        return jsonify(application.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_application_score(app_id):
    """Get application score."""
    try:
        score = db.session.query(ScoreHistory).filter_by(application_id=app_id).first()
        if not score:
            return jsonify({"error": "Score not found"}), 404
        
        return jsonify({"score": score.score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/applications/<int:app_id>', methods=['GET'])
@require_auth
@debug_log
def get_application_route(app_id):
    """Get application by ID."""
    return get_application(app_id)

@app.route('/api/applications/<int:app_id>/score', methods=['GET'])
@require_auth
@debug_log
def get_application_score_route(app_id):
    """Get application score."""
    return get_application_score(app_id)

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
@debug_log
def login():
    """Handle user login"""
    if request.method == 'OPTIONS':
        app.logger.info("[Login] Handling OPTIONS request")
        return '', 204
        
    try:
        app.logger.info("=== Starting login process ===")
        app.logger.info(f"[Login] Request headers: {dict(request.headers)}")
        app.logger.info(f"[Login] Request method: {request.method}")
        app.logger.info(f"[Login] Content-Type: {request.content_type}")
        app.logger.info(f"[Login] Request body: {request.get_data()}")

        data = request.get_json()
        app.logger.info(f"[Login] Parsed request data: {data}")

        if not data or 'username' not in data or 'password' not in data:
            app.logger.warning("[Login] Missing username or password in request data")
            return jsonify({'error': 'Missing username or password'}), 400

        app.logger.info(f"[Login] Attempting authentication for user: {data['username']}")
        result = auth_service.authenticate(data['username'], data['password'])
        app.logger.info(f"[Login] Authentication result: {result is not None}")
        
        if result:
            app.logger.info(f"[Login] Authentication successful for user: {data['username']}")
            app.logger.info("[Login] Creating response with tokens")
            
            response_data = {
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'user': result['user']
            }
            app.logger.info(f"[Login] Response data prepared: {response_data}")
            
            response = jsonify(response_data)
            app.logger.info("[Login] Returning successful login response")
            return response
        else:
            app.logger.warning(f"[Login] Failed authentication for user: {data['username']}")
            return jsonify({
                'error': 'Invalid credentials', 
                'message': 'Invalid username or password'
            }), 401

    except Exception as e:
        app.logger.error(f"[Login] Error during login: {str(e)}")
        app.logger.error(f"[Login] Error traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@app.route('/api/teams', methods=['GET'])
@require_auth
@debug_log
def get_teams():
    """Get all teams with their application counts and average scores"""
    try:
        # Use distinct() to ensure we only get unique teams
        teams = Team.query.distinct().order_by(Team.name).all()
        log_info(f"Retrieved {len(teams)} teams")
        return jsonify([team.to_dict() for team in teams])
    except Exception as e:
        log_error(f"Error fetching teams: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch teams', 'error': str(e)}), 500

@app.route('/api/teams/<int:team_id>/applications', methods=['GET'])
@require_auth
@debug_log
def get_team_applications(team_id):
    """Get all applications for a team with their latest security scores"""
    try:
        team = Team.query.get_or_404(team_id)
        log_info(f"Retrieved applications for team {team_id}")
        return jsonify([app.to_dict() for app in team.applications])
    except Exception as e:
        log_error(f"Error getting team applications: {str(e)}")
        return jsonify({'message': 'Error retrieving team applications'}), 500

@app.route('/api/catalog/applications/search', methods=['GET'])
@debug_log
async def search_catalog_applications():
    """Search applications in the app catalog."""
    query = request.args.get('q', '')
    apps = await app_catalog.search_applications(query)
    log_info(f"Retrieved {len(apps)} applications from catalog")
    return jsonify(apps)

@app.route('/api/applications/sync-catalog', methods=['POST'])
@debug_log
async def sync_applications_with_catalog():
    """Sync local applications with the app catalog."""
    try:
        # Get all applications from catalog
        catalog_apps = await app_catalog.search_applications()
        
        for cat_app in catalog_apps:
            # Check if application exists locally
            app = Application.query.filter_by(catalog_id=cat_app['id']).first()
            
            if app:
                # Update existing application
                app.name = cat_app['name']
                app.description = cat_app.get('description', '')
                app.vendor_name = cat_app.get('vendor', {}).get('name')
                app.vendor_contact = cat_app.get('vendor', {}).get('contact')
                app.support_url = cat_app.get('support_url')
            else:
                # Create new application
                app = Application(
                    catalog_id=cat_app['id'],
                    name=cat_app['name'],
                    description=cat_app.get('description', ''),
                    app_type=cat_app.get('type', 'built'),
                    vendor_name=cat_app.get('vendor', {}).get('name'),
                    vendor_contact=cat_app.get('vendor', {}).get('contact'),
                    support_url=cat_app.get('support_url')
                )
                db.session.add(app)
        
        db.session.commit()
        log_info("Applications synced successfully")
        return jsonify({"message": "Applications synced successfully"})
    except Exception as e:
        db.session.rollback()
        log_error(f"Error syncing applications: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/applications', methods=['GET'])
@require_auth
@debug_log
def get_applications():
    """Get all applications with optional filtering and sorting"""
    try:
        log_info("Fetching applications with filters")
        
        # Get query parameters
        search_query = request.args.get('search', '').lower()
        sort_by = request.args.get('sort', 'name')
        sort_order = request.args.get('order', 'asc')
        team_id = request.args.get('team_id')
        
        # Start with base query - use distinct to ensure unique applications
        query = Application.query.distinct()
        
        # Apply search filter if provided
        if search_query:
            query = query.filter(
                db.or_(
                    Application.name.ilike(f'%{search_query}%'),
                    Application.description.ilike(f'%{search_query}%'),
                    Application.vendor_name.ilike(f'%{search_query}%')
                )
            )
        
        # Apply team filter if provided
        if team_id:
            query = query.filter_by(team_id=team_id)
        
        # Apply sorting
        if sort_by == 'name':
            query = query.order_by(Application.name.asc() if sort_order == 'asc' else Application.name.desc())
        elif sort_by == 'created_at':
            query = query.order_by(Application.created_at.asc() if sort_order == 'asc' else Application.created_at.desc())
        
        # Execute query
        applications = query.all()
        
        # Format response
        result = []
        for app in applications:
            app_dict = app.to_dict()
            app_dict['team'] = {'id': app.team.id, 'name': app.team.name} if app.team else None
            app_dict['security_score'] = round(app.security_score) if app.security_score is not None else 0
            result.append(app_dict)
        
        log_info(f"Successfully fetched {len(result)} applications")
        return jsonify(result)
    except Exception as e:
        log_error(f"Error fetching applications: {str(e)}", exc_info=True)
        return jsonify({'message': 'Failed to fetch applications', 'error': str(e)}), 500

@app.route('/api/applications', methods=['POST'])
@require_auth
@debug_log
def create_application():
    """Create a new application."""
    data = request.json
    
    new_app = Application(
        name=data['name'],
        description=data.get('description', ''),
        app_type=data.get('app_type', 'built'),
        team_id=data.get('team_id')
    )
    
    if new_app.catalog_id:
        # catalog_service.sync_application(new_app)
        pass
    
    db.session.add(new_app)
    db.session.commit()
    
    log_info(f"Created new application: {new_app.name}")
    return jsonify({
        'id': new_app.id,
        'name': new_app.name,
        'description': new_app.description,
        'app_type': new_app.app_type,
        'vendor_name': new_app.vendor_name,
        'vendor_contact': new_app.vendor_contact,
        'support_url': new_app.support_url,
        'created_at': new_app.created_at.isoformat()
    }), 201

@app.route('/api/applications/<int:app_id>/sync', methods=['POST'])
@require_auth
@debug_log
def sync_application_catalog(app_id):
    """Sync application with catalog data."""
    application = Application.query.get_or_404(app_id)
    
    if not application.catalog_id:
        log_warning("Application has no catalog ID")
        return jsonify({'error': 'Application has no catalog ID'}), 400
    
    # catalog_service.sync_application(application)
    db.session.commit()
    
    log_info(f"Synced application {app_id} with catalog")
    return jsonify({
        'id': application.id,
        'name': application.name,
        'description': application.description,
        'app_type': application.app_type,
        'vendor_name': application.vendor_name,
        'vendor_contact': application.vendor_contact,
        'support_url': application.support_url,
        'last_synced': datetime.utcnow().isoformat()
    })

@app.route('/api/applications/<int:app_id>/vulnerabilities', methods=['GET'])
@require_auth
@debug_log
def get_vulnerabilities(app_id):
    vulns = Vulnerability.query.filter_by(application_id=app_id).all()
    log_info(f"Retrieved {len(vulns)} vulnerabilities for application {app_id}")
    return jsonify([{
        'id': vuln.id,
        'title': vuln.title,
        'description': vuln.description,
        'severity': vuln.severity,
        'status': vuln.status,
        'created_at': vuln.created_at.isoformat(),
        'updated_at': vuln.updated_at.isoformat()
    } for vuln in vulns])

@app.route('/api/applications/<int:app_id>/vulnerabilities', methods=['POST'])
@require_auth
@debug_log
def add_vulnerability(app_id):
    data = request.json
    new_vuln = Vulnerability(
        application_id=app_id,
        title=data['title'],
        description=data.get('description', ''),
        severity=data['severity'],
        status=data.get('status', 'OPEN')
    )
    db.session.add(new_vuln)
    db.session.commit()
    
    log_info(f"Added new vulnerability to application {app_id}")
    # Return both the new vulnerability and the updated security score
    app = Application.query.get(app_id)
    return jsonify({
        'vulnerability': {
            'id': new_vuln.id,
            'title': new_vuln.title,
            'description': new_vuln.description,
            'severity': new_vuln.severity,
            'status': new_vuln.status,
            'created_at': new_vuln.created_at.isoformat(),
            'updated_at': new_vuln.updated_at.isoformat()
        },
        'security_score': app.security_score
    }), 201

@app.route('/api/applications/<int:app_id>/vulnerabilities/<int:vuln_id>', methods=['PUT'])
@require_auth
@debug_log
def update_vulnerability(app_id, vuln_id):
    vuln = Vulnerability.query.get_or_404(vuln_id)
    data = request.json
    
    vuln.title = data.get('title', vuln.title)
    vuln.description = data.get('description', vuln.description)
    vuln.severity = data.get('severity', vuln.severity)
    vuln.status = data.get('status', vuln.status)
    
    db.session.commit()
    
    log_info(f"Updated vulnerability {vuln_id} for application {app_id}")
    # Return both the updated vulnerability and the new security score
    app = Application.query.get(app_id)
    return jsonify({
        'vulnerability': {
            'id': vuln.id,
            'title': vuln.title,
            'description': vuln.description,
            'severity': vuln.severity,
            'status': vuln.status,
            'created_at': vuln.created_at.isoformat(),
            'updated_at': vuln.updated_at.isoformat()
        },
        'security_score': app.security_score
    })

@app.route('/api/groups', methods=['GET'])
@require_auth
@debug_log
def get_groups():
    """Get all application groups."""
    groups = ApplicationGroup.query.all()
    log_info(f"Retrieved {len(groups)} groups")
    return jsonify([{
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'created_at': group.created_at.isoformat(),
        'applications': [{
            'id': app.id,
            'name': app.name,
            'security_score': app.security_score
        } for app in group.applications]
    } for group in groups])

@app.route('/api/groups', methods=['POST'])
@require_auth
@debug_log
def create_group():
    """Create a new application group."""
    data = request.json
    new_group = ApplicationGroup(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_group)
    db.session.commit()
    
    log_info(f"Created new group: {new_group.name}")
    return jsonify({
        'id': new_group.id,
        'name': new_group.name,
        'description': new_group.description,
        'created_at': new_group.created_at.isoformat(),
        'applications': []
    }), 201

@app.route('/api/groups/<int:group_id>/applications', methods=['POST'])
@require_auth
@debug_log
def add_application_to_group(group_id):
    """Add an application to a group."""
    data = request.json
    app_id = data['application_id']
    
    group = ApplicationGroup.query.get_or_404(group_id)
    application = Application.query.get_or_404(app_id)
    
    if application not in group.applications:
        group.applications.append(application)
        db.session.commit()
    
    log_info(f"Added application {app_id} to group {group_id}")
    return jsonify({
        'id': group.id,
        'name': group.name,
        'applications': [{
            'id': app.id,
            'name': app.name,
            'security_score': app.security_score
        } for app in group.applications]
    })

@app.route('/api/groups/<int:group_id>/applications/<int:app_id>', methods=['DELETE'])
@require_auth
@debug_log
def remove_application_from_group(group_id, app_id):
    """Remove an application from a group."""
    group = ApplicationGroup.query.get_or_404(group_id)
    application = Application.query.get_or_404(app_id)
    
    if application in group.applications:
        group.applications.remove(application)
        db.session.commit()
    
    log_info(f"Removed application {app_id} from group {group_id}")
    return jsonify({
        'id': group.id,
        'name': group.name,
        'applications': [{
            'id': app.id,
            'name': app.name,
            'security_score': app.security_score
        } for app in group.applications]
    })

@app.route('/api/groups/<int:group_id>/score', methods=['GET'])
@require_auth
@debug_log
def get_group_score(group_id):
    """Get aggregated security score for a group."""
    group = ApplicationGroup.query.get_or_404(group_id)
    
    if not group.applications:
        log_info(f"Group {group_id} has no applications")
        return jsonify({
            'group_id': group_id,
            'average_score': 0,
            'applications': []
        })
    
    app_scores = [{
        'id': app.id,
        'name': app.name,
        'score': app.security_score,
        'findings': SecurityScore.query.filter_by(application_id=app.id)
            .order_by(SecurityScore.created_at.desc())
            .first().findings if SecurityScore.query.filter_by(application_id=app.id).first() else None
    } for app in group.applications]
    
    average_score = sum(app['score'] for app in app_scores) / len(app_scores)
    
    log_info(f"Calculated average score for group {group_id}: {average_score}")
    return jsonify({
        'group_id': group_id,
        'average_score': round(average_score, 2),
        'applications': app_scores
    })

@app.route('/api/applications/<int:app_id>/generate-score', methods=['POST'])
@require_auth
@debug_log
def generate_application_score(app_id):
    """Generate a security score for a single application."""
    try:
        application = Application.query.get_or_404(app_id)
        
        # Get application metadata from request
        data = request.json or {}
        
        # Collect scoring factors
        factors = {
            "vulnerabilities": {
                "critical_count": len([v for v in application.vulnerabilities if v.severity == "CRITICAL"]),
                "high_count": len([v for v in application.vulnerabilities if v.severity == "HIGH"]),
                "medium_count": len([v for v in application.vulnerabilities if v.severity == "MEDIUM"]),
                "low_count": len([v for v in application.vulnerabilities if v.severity == "LOW"])
            },
            "metadata": {
                "platform": data.get('platform'),
                "team": data.get('team'),
                "environment": data.get('environment'),
                "criticality": data.get('criticality', 'medium'),
                "last_assessment": data.get('last_assessment'),
                "compliance_status": data.get('compliance_status', {})
            },
            "security_controls": {
                "mfa_enabled": data.get('mfa_enabled', False),
                "encryption_at_rest": data.get('encryption_at_rest', False),
                "waf_enabled": data.get('waf_enabled', False),
                "ssl_enabled": data.get('ssl_enabled', False),
                "access_control": data.get('access_control', 'basic'),
                "logging_enabled": data.get('logging_enabled', False),
                "monitoring_enabled": data.get('monitoring_enabled', False)
            }
        }
        
        # Calculate base score (100)
        score = 100
        
        # Deduct for vulnerabilities
        score -= factors['vulnerabilities']['critical_count'] * 15
        score -= factors['vulnerabilities']['high_count'] * 10
        score -= factors['vulnerabilities']['medium_count'] * 5
        score -= factors['vulnerabilities']['low_count'] * 2
        
        # Adjust for security controls
        if not factors['security_controls']['mfa_enabled']:
            score -= 10
        if not factors['security_controls']['encryption_at_rest']:
            score -= 10
        if not factors['security_controls']['waf_enabled']:
            score -= 5
        if not factors['security_controls']['ssl_enabled']:
            score -= 10
        if factors['security_controls']['access_control'] == 'basic':
            score -= 5
        if not factors['security_controls']['logging_enabled']:
            score -= 5
        if not factors['security_controls']['monitoring_enabled']:
            score -= 5
            
        # Adjust for compliance and assessment
        if not factors['metadata'].get('last_assessment'):
            score -= 10
        
        compliance_status = factors['metadata']['compliance_status']
        if compliance_status:
            non_compliant_items = sum(1 for status in compliance_status.values() if not status)
            score -= non_compliant_items * 5
        
        # Ensure score stays within 0-100 range
        final_score = max(0, min(100, score))
        
        # Create score record
        new_score = SecurityScore(
            application_id=app_id,
            score=final_score,
            category="Overall",
            findings={
                "factors": factors,
                "deductions": {
                    "vulnerabilities": 100 - score,
                    "security_controls": sum([
                        10 if not factors['security_controls']['mfa_enabled'] else 0,
                        10 if not factors['security_controls']['encryption_at_rest'] else 0,
                        5 if not factors['security_controls']['waf_enabled'] else 0,
                        10 if not factors['security_controls']['ssl_enabled'] else 0,
                        5 if factors['security_controls']['access_control'] == 'basic' else 0,
                        5 if not factors['security_controls']['logging_enabled'] else 0,
                        5 if not factors['security_controls']['monitoring_enabled'] else 0
                    ]),
                    "compliance": len(compliance_status) * 5 if compliance_status else 0
                }
            }
        )
        db.session.add(new_score)
        db.session.commit()
        
        log_info(f"Generated security score for application {app_id}: {final_score}")
        return jsonify({
            "application_id": app_id,
            "name": application.name,
            "score": round(final_score),
            "timestamp": datetime.utcnow().isoformat(),
            "factors": factors,
            "findings": new_score.findings
        })
        
    except Exception as e:
        log_error(f"Error generating security score for application {app_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/groups/<int:group_id>/generate-score', methods=['POST'])
@require_auth
@debug_log
def generate_group_score(group_id):
    """Generate a security score for a group of applications."""
    try:
        group = ApplicationGroup.query.get_or_404(group_id)
        
        if not group.applications:
            log_info(f"Group {group_id} has no applications")
            return jsonify({
                "group_id": group_id,
                "name": group.name,
                "score": 0,
                "applications": [],
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Get group metadata from request
        data = request.json or {}
        
        # Generate scores for all applications in the group
        application_scores = []
        for app in group.applications:
            app_score = generate_application_score(app.id).get_json()
            application_scores.append(app_score)
        
        # Calculate group statistics
        total_score = sum(app['score'] for app in application_scores)
        avg_score = total_score / len(application_scores)
        min_score = min(app['score'] for app in application_scores)
        max_score = max(app['score'] for app in application_scores)
        
        # Aggregate vulnerability counts
        total_vulns = {
            "critical": sum(app['factors']['vulnerabilities']['critical_count'] for app in application_scores),
            "high": sum(app['factors']['vulnerabilities']['high_count'] for app in application_scores),
            "medium": sum(app['factors']['vulnerabilities']['medium_count'] for app in application_scores),
            "low": sum(app['factors']['vulnerabilities']['low_count'] for app in application_scores)
        }
        
        # Calculate compliance percentage
        compliant_apps = sum(1 for app in application_scores 
                           if not any(app['factors']['metadata']['compliance_status'].values()))
        compliance_percentage = (compliant_apps / len(application_scores)) * 100
        
        result = {
            "group_id": group_id,
            "name": group.name,
            "score": round(avg_score),
            "statistics": {
                "minimum_score": min_score,
                "maximum_score": max_score,
                "average_score": round(avg_score),
                "total_applications": len(application_scores),
                "compliance_percentage": round(compliance_percentage)
            },
            "risk_summary": {
                "total_vulnerabilities": total_vulns,
                "high_risk_applications": len([app for app in application_scores if app['score'] < 70]),
                "medium_risk_applications": len([app for app in application_scores if 70 <= app['score'] < 90]),
                "low_risk_applications": len([app for app in application_scores if app['score'] >= 90])
            },
            "applications": application_scores,
            "metadata": {
                "type": data.get('type', 'platform'),  # platform or team
                "owner": data.get('owner'),
                "last_assessment": datetime.utcnow().isoformat(),
                "tags": data.get('tags', [])
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        log_info(f"Generated security score for group {group_id}: {avg_score}")
        return jsonify(result)
        
    except Exception as e:
        log_error(f"Error generating security score for group {group_id}: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/api/applications/<int:app_id>/findings', methods=['GET'])
@require_auth
@debug_log
def get_findings(app_id):
    """Get all findings for an application."""
    findings = Finding.query.filter_by(application_id=app_id).all()
    application = Application.query.get_or_404(app_id)
    
    log_info(f"Retrieved {len(findings)} findings for application {app_id}")
    return jsonify([{
        'id': f.id,
        'title': f.title,
        'applicationName': application.name,
        'severity': f.severity,
        'status': f.status,
        'dateOpen': f.date_open.isoformat(),
        'plannedCloseDate': f.planned_close_date.isoformat() if f.planned_close_date else None,
        'actualCloseDate': f.actual_close_date.isoformat() if f.actual_close_date else None,
        'comments': f.comments,
        'created_at': f.created_at.isoformat(),
        'updated_at': f.updated_at.isoformat()
    } for f in findings])

@app.route('/api/applications/<int:app_id>/findings', methods=['POST'])
@require_auth
@debug_log
def create_finding(app_id):
    """Create a new finding."""
    data = request.json
    
    new_finding = Finding(
        application_id=app_id,
        title=data['title'],
        severity=data['severity'],
        status=data['status'],
        date_open=datetime.fromisoformat(data.get('dateOpen', datetime.utcnow().isoformat())),
        planned_close_date=datetime.fromisoformat(data['plannedCloseDate']) if data.get('plannedCloseDate') else None,
        comments=data.get('comments', '')
    )
    
    db.session.add(new_finding)
    db.session.commit()
    
    log_info(f"Created new finding for application {app_id}")
    return jsonify({
        'id': new_finding.id,
        'title': new_finding.title,
        'severity': new_finding.severity,
        'status': new_finding.status,
        'dateOpen': new_finding.date_open.isoformat(),
        'plannedCloseDate': new_finding.planned_close_date.isoformat() if new_finding.planned_close_date else None,
        'comments': new_finding.comments,
        'created_at': new_finding.created_at.isoformat()
    }), 201

@app.route('/api/applications/<int:app_id>/findings/<int:finding_id>', methods=['PUT'])
@require_auth
@debug_log
def update_finding(app_id, finding_id):
    """Update a finding."""
    finding = Finding.query.filter_by(id=finding_id, application_id=app_id).first_or_404()
    data = request.json
    
    if 'title' in data:
        finding.title = data['title']
    if 'severity' in data:
        finding.severity = data['severity']
    if 'status' in data:
        finding.status = data['status']
    if 'plannedCloseDate' in data:
        finding.planned_close_date = datetime.fromisoformat(data['plannedCloseDate'])
    if 'comments' in data:
        finding.comments = data['comments']
    if data.get('status') == 'CLOSED' and finding.status != 'CLOSED':
        finding.actual_close_date = datetime.utcnow()
    
    db.session.commit()
    
    log_info(f"Updated finding {finding_id} for application {app_id}")
    return jsonify({
        'id': finding.id,
        'title': finding.title,
        'severity': finding.severity,
        'status': finding.status,
        'dateOpen': finding.date_open.isoformat(),
        'plannedCloseDate': finding.planned_close_date.isoformat() if finding.planned_close_date else None,
        'actualCloseDate': finding.actual_close_date.isoformat() if finding.actual_close_date else None,
        'comments': finding.comments,
        'updated_at': finding.updated_at.isoformat()
    })

@app.route('/api/applications/<int:app_id>/score-history', methods=['GET'])
@require_auth
@debug_log
def get_score_history(app_id):
    """Get score history for an application."""
    scores = ScoreHistory.query.filter_by(application_id=app_id)\
        .order_by(ScoreHistory.created_at.asc())\
        .all()
    
    log_info(f"Retrieved {len(scores)} scores for application {app_id}")
    return jsonify([{
        'score': score.score,
        'timestamp': score.created_at.isoformat(),
        'findings': score.findings
    } for score in scores])

@app.route('/api/applications/search', methods=['GET'])
@require_auth
@debug_log
def search_applications():
    """Search applications with filtering and sorting."""
    # Search parameters
    name = request.args.get('name')
    team_name = request.args.get('team')
    app_type = request.args.get('type')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    # Base query
    query = db.session.query(Application)

    # Apply filters
    if name:
        query = query.filter(Application.name.ilike(f'%{name}%'))
    if team_name:
        query = query.join(Application.team).filter(Team.name.ilike(f'%{team_name}%'))
    if app_type:
        query = query.filter(Application.app_type == app_type)

    # Apply sorting
    if sort_by == 'name':
        query = query.order_by(Application.name.asc() if sort_order == 'asc' else Application.name.desc())
    elif sort_by == 'type':
        query = query.order_by(Application.app_type.asc() if sort_order == 'asc' else Application.app_type.desc())
    elif sort_by == 'created_at':
        query = query.order_by(Application.created_at.asc() if sort_order == 'asc' else Application.created_at.desc())
    elif sort_by == 'score':
        # For score sorting, we need to join with the latest scores
        latest_scores = db.session.query(
            ScoreHistory.application_id,
            db.func.max(ScoreHistory.created_at).label('max_date')
        ).group_by(ScoreHistory.application_id).subquery()
        
        query = query.join(
            latest_scores,
            Application.id == latest_scores.c.application_id
        ).join(
            ScoreHistory,
            and_(
                ScoreHistory.application_id == latest_scores.c.application_id,
                ScoreHistory.created_at == latest_scores.c.max_date
            )
        ).order_by(ScoreHistory.score.asc() if sort_order == 'asc' else ScoreHistory.score.desc())

    # Pagination
    paginated_apps = query.paginate(page=page, per_page=per_page, error_out=False)
    
    log_info(f"Retrieved {len(paginated_apps.items)} applications")
    return jsonify({
        'applications': [{
            'id': app.id,
            'name': app.name,
            'description': app.description,
            'app_type': app.app_type,
            'vendor_name': app.vendor_name,
            'teams': [{'id': team.id, 'name': team.name} for team in app.team.applications],
            'security_score': round(app.security_score) if app.security_score is not None else 0,
            'created_at': app.created_at.isoformat()
        } for app in paginated_apps.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': paginated_apps.pages,
            'total_items': paginated_apps.total
        }
    })

@app.route('/api/teams', methods=['POST'])
@require_auth
@debug_log
def create_team():
    """Create a new team."""
    data = request.json
    new_team = Team(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(new_team)
    db.session.commit()
    
    log_info(f"Created new team: {new_team.name}")
    return jsonify({
        'id': new_team.id,
        'name': new_team.name,
        'description': new_team.description,
        'created_at': new_team.created_at.isoformat()
    }), 201

@app.route('/api/teams/<int:team_id>', methods=['PUT'])
@require_auth
@debug_log
def update_team(team_id):
    """Update a team."""
    team = Team.query.get_or_404(team_id)
    data = request.json
    
    if 'name' in data:
        team.name = data['name']
    if 'description' in data:
        team.description = data['description']
    
    db.session.commit()
    
    log_info(f"Updated team {team_id}")
    return jsonify({
        'id': team.id,
        'name': team.name,
        'description': team.description,
        'created_at': team.created_at.isoformat()
    })

@app.route('/api/teams/<int:team_id>', methods=['DELETE'])
@require_auth
@debug_log
def delete_team(team_id):
    """Delete a team."""
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    
    log_info(f"Deleted team {team_id}")
    return '', 204

@app.route('/api/applications/<int:app_id>/teams', methods=['POST'])
@require_auth
@debug_log
def add_team_to_application(app_id):
    """Add a team to an application."""
    data = request.json
    application = Application.query.get_or_404(app_id)
    team = Team.query.get_or_404(data['team_id'])
    
    app_team = ApplicationTeam(
        application_id=app_id,
        team_id=data['team_id'],
        role=data.get('role', 'member')
    )
    
    db.session.add(app_team)
    db.session.commit()
    
    log_info(f"Added team {team.id} to application {app_id}")
    return jsonify({
        'application_id': app_id,
        'team_id': team.id,
        'team_name': team.name,
        'role': app_team.role
    }), 201

@app.route('/api/applications/<int:app_id>/teams/<int:team_id>', methods=['DELETE'])
@require_auth
@debug_log
def remove_team_from_application(app_id, team_id):
    """Remove a team from an application."""
    app_team = ApplicationTeam.query.filter_by(
        application_id=app_id,
        team_id=team_id
    ).first_or_404()
    
    db.session.delete(app_team)
    db.session.commit()
    
    log_info(f"Removed team {team_id} from application {app_id}")
    return '', 204

@app.route('/api/applications/<int:app_id>/remediations', methods=['GET'])
@require_auth
@debug_log
def get_application_remediations(app_id):
    """Get remediation recommendations for an application"""
    try:
        # Get the latest score history entry
        latest_score = ScoreHistory.query.filter_by(application_id=app_id).order_by(ScoreHistory.created_at.desc()).first()
        
        if not latest_score:
            log_info(f"No score history found for application {app_id}")
            return jsonify([])
            
        # Return a default set of remediations
        log_info(f"Returning default remediations for application {app_id}")
        return jsonify([
            {
                'id': 1,
                'title': 'Review security configurations',
                'description': 'Regularly review and update security configurations',
                'status': 'Pending',
                'priority': 'High',
                'created_at': latest_score.created_at.isoformat() if latest_score.created_at else None
            },
            {
                'id': 2,
                'title': 'Update dependencies',
                'description': 'Keep all dependencies up to date',
                'status': 'Pending',
                'priority': 'Medium',
                'created_at': latest_score.created_at.isoformat() if latest_score.created_at else None
            }
        ])
    except Exception as e:
        log_error(f"Error fetching remediations for application {app_id}: {str(e)}", exc_info=True)
        return jsonify({'message': f'Failed to fetch remediations', 'error': str(e)}), 500

@app.route('/api/teams/<int:team_id>', methods=['GET'])
@require_auth
@debug_log
def get_team(team_id):
    """Get a single team by ID."""
    try:
        team = Team.query.get_or_404(team_id)
        log_info(f"Retrieved team {team_id}")
        return jsonify(team.to_dict())
    except Exception as e:
        log_error(f"Error getting team: {str(e)}")
        return jsonify({'error': 'Failed to fetch team'}), 500

@app.route('/api/teams/<int:team_id>/score-history', methods=['GET'])
@require_auth
@debug_log
def get_team_score_history(team_id):
    """Get score history for all applications in a team."""
    try:
        # Get all applications for the team
        team = Team.query.get_or_404(team_id)
        app_ids = [app.id for app in team.applications]
        
        # Get score history for each application
        history = (
            db.session.query(
                ScoreHistory.created_at,
                db.func.avg(ScoreHistory.score).label('score')
            )
            .filter(ScoreHistory.application_id.in_(app_ids))
            .group_by(ScoreHistory.created_at)
            .order_by(ScoreHistory.created_at)
            .limit(30)  # Last 30 data points
            .all()
        )
        
        log_info(f"Retrieved score history for team {team_id}")
        return jsonify([{
            'date': entry.created_at.isoformat(),
            'score': round(entry.score)
        } for entry in history])
    except Exception as e:
        log_error(f"Error getting team score history: {str(e)}")
        return jsonify({'error': 'Failed to fetch team score history'}), 500

@app.route('/api/teams/<int:team_id>/todo', methods=['GET'])
@require_auth
@debug_log
def get_team_todo(team_id):
    """Get TODO items for a team based on findings and vulnerabilities."""
    try:
        # Get all applications for the team
        team = Team.query.get_or_404(team_id)
        
        todo_items = []
        for app in team.applications:
            # Get open findings for the application
            findings = Finding.query.filter_by(
                application_id=app.id,
                status='OPEN'
            ).order_by(Finding.severity.desc()).all()
            
            # Add findings to TODO list
            for finding in findings:
                todo_items.append({
                    'type': 'Finding',
                    'title': finding.title,
                    'severity': finding.severity,
                    'application': app.name,
                    'days_open': (datetime.utcnow() - finding.created_at).days,
                    'due_date': finding.planned_close_date.isoformat() if finding.planned_close_date else None
                })
            
            # Get open vulnerabilities for the application
            vulns = Vulnerability.query.filter_by(
                application_id=app.id,
                status='OPEN'
            ).order_by(Vulnerability.severity.desc()).all()
            
            # Add vulnerabilities to TODO list
            for vuln in vulns:
                todo_items.append({
                    'type': 'Vulnerability',
                    'title': vuln.title,
                    'severity': vuln.severity,
                    'application': app.name,
                    'days_open': (datetime.utcnow() - vuln.created_at).days,
                    'due_date': vuln.planned_close_date.isoformat() if vuln.planned_close_date else None
                })
        
        # Sort by severity and days open
        todo_items.sort(key=lambda x: (
            {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}.get(x['severity'], 4),
            x['days_open']
        ), reverse=True)
        
        log_info(f"Retrieved TODO items for team {team_id}")
        return jsonify(todo_items)
    except Exception as e:
        log_error(f"Error getting team TODO items: {str(e)}")
        return jsonify({'error': 'Failed to fetch team TODO items'}), 500

@app.route('/api/applications/<int:app_id>/findings', methods=['GET'])
@require_auth
@debug_log
def get_application_findings(app_id):
    """Get application findings."""
    try:
        findings = Finding.query.filter_by(application_id=app_id).all()
        log_info(f"Retrieved {len(findings)} findings for application {app_id}")
        return jsonify([finding.to_dict() for finding in findings])
    except Exception as e:
        log_error(f"Error fetching findings for application {app_id}: {str(e)}", exc_info=True)
        return jsonify({'message': f'Failed to fetch findings', 'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>/scores', methods=['GET'])
@require_auth
@debug_log
def get_application_scores(app_id):
    """Get security scores for an application."""
    try:
        scores = ScoreHistory.query.filter_by(application_id=app_id).order_by(ScoreHistory.created_at.desc()).all()
        result = []
        for score in scores:
            result.append({
                'id': score.id,
                'score': score.score,
                'created_at': score.created_at.isoformat() if score.created_at else None
            })
        log_info(f"Retrieved {len(result)} scores for application {app_id}")
        return jsonify(result)
    except Exception as e:
        log_error(f"Error fetching scores for application {app_id}: {str(e)}", exc_info=True)
        return jsonify({'message': f'Failed to fetch scores for application {app_id}', 'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>/team', methods=['PUT'])
@require_auth
@debug_log
def update_application_team(app_id):
    """Update an application's team"""
    try:
        data = request.get_json()
        new_team_id = data.get('team_id')
        
        if new_team_id is None:
            log_warning("team_id is required")
            return jsonify({'message': 'team_id is required'}), 400
            
        application = db.session.query(Application).get(app_id)
        if not application:
            log_warning(f"Application not found: {app_id}")
            return jsonify({'message': 'Application not found'}), 404
            
        # Check if new team exists
        new_team = db.session.query(Team).get(new_team_id)
        if not new_team:
            log_warning(f"Team not found: {new_team_id}")
            return jsonify({'message': 'Team not found'}), 404
            
        # Update the team
        application.team_id = new_team_id
        db.session.commit()
        
        log_info(f"Updated team for application {app_id}")
        return jsonify({
            'message': 'Application team updated successfully',
            'application': {
                'id': application.id,
                'name': application.name,
                'team_id': application.team_id
            }
        })
        
    except Exception as e:
        db.session.rollback()
        log_error(f"Error updating application team: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/api/auth/refresh', methods=['POST', 'OPTIONS'])
@debug_log
def refresh_token():
    """Refresh the access token using a valid refresh token"""
    if request.method == 'OPTIONS':
        return '', 204

    try:
        # Get refresh token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            log_warning("No refresh token provided")
            return jsonify({'error': 'No refresh token provided'}), 401

        refresh_token = auth_header.split(' ')[1]
        log_info("Attempting to refresh token")

        # Verify refresh token and get user
        user = auth_service.verify_refresh_token(refresh_token)
        if not user:
            log_warning("Invalid refresh token")
            return jsonify({'error': 'Invalid refresh token'}), 401

        # Generate new tokens
        result = auth_service.authenticate(user.username, refresh=True)
        if not result:
            log_error("Failed to generate new tokens")
            return jsonify({'error': 'Failed to generate new tokens'}), 500

        log_info("Successfully refreshed tokens")
        return jsonify({
            'access_token': result['access_token'],
            'refresh_token': result['refresh_token']
        })

    except Exception as e:
        log_error(f"Token refresh error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>/details', methods=['GET'])
@require_auth
@debug_log
def get_application_details(app_id):
    """Get a single application by ID with detailed information."""
    try:
        application = Application.query.get_or_404(app_id)
        return jsonify({
            'status': 'success',
            'data': application.to_dict(include_teams=True, include_scores=True)
        }), 200
    except Exception as e:
        log_error(f"Error getting application details: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/auth/validate', methods=['POST'])
@debug_log
def validate_token():
    """Validate the access token"""
    try:
        log_info("=== Starting token validation ===")
        log_info(f"Request headers: {dict(request.headers)}")
        
        auth_header = request.headers.get('Authorization')
        log_info(f"[Validate] Authorization header: {auth_header}")
        
        if not auth_header or not auth_header.startswith('Bearer '):
            log_warning("[Validate] No Bearer token found in Authorization header")
            return jsonify({'valid': False, 'error': 'No token provided'}), 401
            
        token = auth_header.split(' ')[1]
        log_info(f"[Validate] Token to validate: {token[:20]}...")
        
        try:
            # Decode and verify the token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            log_info(f"[Validate] Token payload: {payload}")
            log_info(f"[Validate] Token expiration: {datetime.fromtimestamp(payload['exp'])}")
            
            # Check if user exists and is active
            user = User.query.get(payload['user_id'])
            if not user:
                log_warning(f"[Validate] User not found: {payload['user_id']}")
                return jsonify({'valid': False, 'error': 'User not found'}), 401
                
            if not user.is_active:
                log_warning(f"[Validate] User is inactive: {payload['user_id']}")
                return jsonify({'valid': False, 'error': 'User is inactive'}), 401
            
            log_info(f"[Validate] Token is valid for user: {user.username}")
            return jsonify({
                'valid': True, 
                'user': user.to_dict(),
                'exp': payload['exp']
            })
            
        except jwt.ExpiredSignatureError:
            log_warning("[Validate] Token has expired")
            return jsonify({'valid': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            log_warning(f"[Validate] Invalid token: {str(e)}")
            return jsonify({'valid': False, 'error': 'Invalid token'}), 401
            
    except Exception as e:
        log_error(f"[Validate] Error during token validation: {str(e)}")
        log_error(f"[Validate] Error traceback: {traceback.format_exc()}")
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.cli.command("create-admin")
def create_admin():
    """Create admin user if it doesn't exist"""
    try:
        admin = User.query.filter_by(username='admin').first()
        if admin:
            log_info("Admin user already exists")
            return
        
        admin = User(
            username='admin',
            email='admin@example.com',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        log_info("Admin user created successfully")
    except Exception as e:
        log_error(f"Error creating admin user: {str(e)}")
        db.session.rollback()

@app.cli.command("seed-data")
def seed_data():
    """Seed the database with sample data."""
    # Initialize database
    db.create_all()

    log_info("Clearing existing data...")
    Application.query.delete()
    Team.query.delete()
    db.session.commit()

    log_info("Creating sample teams...")
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

    log_info("Creating sample applications...")
    current_time = datetime.utcnow()
    
    applications = [
        Application(
            name="Customer Portal",
            description="Main customer-facing web application",
            app_type=ApplicationType.WEB,
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
            app_type=ApplicationType.WEB,
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
            app_type=ApplicationType.API,
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
            app_type=ApplicationType.API,
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
    log_info(f"Created {len(applications)} applications")

@app.route('/api/reports/team/<team_name>', methods=['GET'])
@debug_log
def generate_team_report(team_name):
    """Generate a detailed report for a team."""
    try:
        report_format = request.args.get('format', 'json')
        report_service = ReportService(db.session)
        
        report_data = report_service.generate_team_report(team_name)
        
        if report_format == 'pdf':
            pdf_data = report_service.convert_to_pdf(report_data, "Team")
            return send_file(
                io.BytesIO(pdf_data),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'team_report_{team_name}.pdf'
            )
        
        return jsonify(report_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/reports/application/<int:app_id>', methods=['GET'])
@debug_log
def generate_application_report(app_id):
    """Generate a detailed report for an application."""
    try:
        report_format = request.args.get('format', 'json')
        report_service = ReportService(db.session)
        
        report_data = report_service.generate_application_report(app_id)
        
        if report_format == 'pdf':
            pdf_data = report_service.convert_to_pdf(report_data, "Application")
            return send_file(
                io.BytesIO(pdf_data),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'application_report_{app_id}.pdf'
            )
        
        return jsonify(report_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/reports/vulnerabilities/<int:app_id>', methods=['GET'])
@debug_log
def generate_vulnerability_report(app_id):
    """Generate a vulnerability report for an application."""
    try:
        report_format = request.args.get('format', 'json')
        report_service = ReportService(db.session)
        
        report_data = report_service.generate_vulnerability_report(app_id)
        
        if report_format == 'pdf':
            pdf_data = report_service.convert_to_pdf(report_data, "Vulnerability")
            return send_file(
                io.BytesIO(pdf_data),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'vulnerability_report_{app_id}.pdf'
            )
        elif report_format == 'csv':
            csv_data = report_service.convert_to_csv(report_data, "Vulnerability")
            return send_file(
                io.BytesIO(csv_data),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'vulnerability_report_{app_id}.csv'
            )
        
        return jsonify(report_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/risk-parameters', methods=['GET'])
@require_auth
@debug_log
def get_risk_parameters():
    """Get the current risk parameters"""
    try:
        params = RiskParameters.get_default()
        log_info("Retrieved risk parameters")
        return jsonify(params.to_dict()), 200
    except Exception as e:
        log_error(f"Error getting risk parameters: {str(e)}")
        return jsonify({'error': 'Failed to get risk parameters'}), 500

@app.route('/api/risk-parameters', methods=['PUT'])
@require_auth
@debug_log
def update_risk_parameters():
    """Update risk parameters"""
    try:
        data = request.get_json()
        params = RiskParameters.get_default()

        # Update weights and thresholds if provided
        if 'built_weights' in data:
            params.built_weights = data['built_weights']
        if 'built_thresholds' in data:
            params.built_thresholds = data['built_thresholds']
        if 'purchased_weights' in data:
            params.purchased_weights = data['purchased_weights']
        if 'purchased_thresholds' in data:
            params.purchased_thresholds = data['purchased_thresholds']

        db.session.commit()
        log_info("Updated risk parameters")
        return jsonify(params.to_dict()), 200
    except Exception as e:
        log_error(f"Error updating risk parameters: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update risk parameters'}), 500

@app.route('/api/applications/<int:app_id>/calculate-risk', methods=['POST'])
@require_auth
@debug_log
def calculate_application_risk(app_id):
    """Calculate risk score for an application"""
    try:
        application = Application.query.get(app_id)
        if not application:
            log_warning(f"Application not found: {app_id}")
            return jsonify({'error': 'Application not found'}), 404

        risk_params = RiskParameters.get_default()
        score = application.calculate_risk_score(risk_params)

        # Update the application's security score
        application.security_score = score
        application.last_scored = datetime.utcnow()
        db.session.commit()

        log_info(f"Calculated risk score for application {app_id}: {score}")
        return jsonify({
            'application_id': app_id,
            'security_score': score,
            'last_scored': application.last_scored.isoformat()
        }), 200
    except Exception as e:
        log_error(f"Error calculating risk score: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to calculate risk score'}), 500

@app.cli.command("db-init")
def db_init():
    """Initialize the database with migrations and seed data."""
    try:
        log_info("Initializing database...")
        
        # Run migrations
        with app.app_context():
            log_info("Running database migrations...")
            from flask_migrate import upgrade
            upgrade()
            
            log_info("Creating seed data...")
            from scripts.seed_data import create_seed_data
            create_seed_data()
            
        log_info("Database initialization completed successfully")
    except Exception as e:
        log_error(f"Error initializing database: {str(e)}", exc_info=True)
        raise

@app.route('/api/admin/seed', methods=['POST'])
@jwt_required()
def seed_database():
    """Endpoint to seed the database with test data.
    Requires admin privileges.
    Returns:
        JSON response indicating success or failure
    """
    try:
        # Check if user has admin role
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({'error': 'Admin privileges required'}), 403

        from scripts.seed_data import create_seed_data
        create_seed_data()
        return jsonify({'message': 'Database seeded successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error seeding database: {str(e)}")
        return jsonify({'error': f'Failed to seed database: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    log_info(f"Starting application in {config.APP_ENV.value} mode")
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
