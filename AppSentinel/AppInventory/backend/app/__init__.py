from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta, datetime
import os
import logging
from sqlalchemy import text
from app.utils.logger import logger
import traceback

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    logger.debug(f"[user_identity_lookup] Converting user identity: {user}")
    return str(user)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    logger.debug(f"[user_lookup_callback] Looking up user with identity: {identity}")
    from app.models.user import User
    try:
        user = User.query.filter_by(id=int(identity)).one_or_none()
        if user:
            logger.debug(f"[user_lookup_callback] Found user: {user.username}")
            return user
        else:
            logger.error(f"[user_lookup_callback] No user found with id: {identity}")
            return None
    except (ValueError, TypeError) as e:
        logger.error(f"[user_lookup_callback] Error converting identity to int: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"[user_lookup_callback] Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return None

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    logger.debug(f"[check_if_token_in_blocklist] Checking token: {jwt_payload}")
    return False

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    logger.info(f"[expired_token_callback] Token expired: {jwt_payload}")
    return jsonify({"message": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    logger.info(f"[invalid_token_callback] Invalid token: {reason}")
    logger.debug(f"[invalid_token_callback] Request headers: {dict(request.headers)}")
    return jsonify({"message": "Invalid token"}), 401

@jwt.unauthorized_loader
def unauthorized_callback(reason):
    logger.info(f"[unauthorized_callback] Unauthorized: {reason}")
    logger.debug(f"[unauthorized_callback] Request headers: {dict(request.headers)}")
    return jsonify({"message": "Missing Authorization Header"}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    logger.info(f"[needs_fresh_token_callback] Fresh token required: {jwt_payload}")
    return jsonify({"message": "Fresh token required"}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    logger.info(f"[revoked_token_callback] Token revoked: {jwt_payload}")
    return jsonify({"message": "Token has been revoked"}), 401

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "supports_credentials": True
        }
    })

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_object('config.Config')
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Initialize Celery
    from .celery_app import create_celery_app
    celery = create_celery_app(app)
    app.celery = celery

    # Register blueprints
    from .routes import auth, applications, departments
    app.register_blueprint(auth.bp)
    app.register_blueprint(applications.bp)
    app.register_blueprint(departments.bp)

    # Add health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db.session.execute(text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500

    # Schedule periodic tasks
    with app.app_context():
        logger.info("Setting up periodic tasks")
        celery.conf.beat_schedule = {
            'check-applications-every-5-minutes': {
                'task': 'tasks.schedule_health_checks',
                'schedule': 300.0,  # 5 minutes
            },
        }

    return app

__all__ = ['db', 'migrate', 'jwt', 'create_app']