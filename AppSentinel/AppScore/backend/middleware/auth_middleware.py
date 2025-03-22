from functools import wraps
from flask import request, jsonify, current_app
from services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("No Authorization header present")
            return jsonify({'message': 'No authorization token provided'}), 401
        
        try:
            # Extract token from Bearer scheme
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                logger.warning(f"Invalid token type: {token_type}")
                return jsonify({'message': 'Invalid token type'}), 401
            
            # Verify token
            auth_service = AuthService(current_app.db.session, current_app.config['SECRET_KEY'])
            payload = auth_service.verify_token(token)
            
            if not payload:
                logger.warning("Invalid or expired token")
                return jsonify({'message': 'Invalid or expired token'}), 401
            
            # Add user info to request context
            request.user = payload
            return f(*args, **kwargs)
            
        except ValueError:
            logger.warning("Malformed Authorization header")
            return jsonify({'message': 'Invalid authorization header format'}), 401
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'message': 'Authentication failed'}), 401
            
    return decorated
