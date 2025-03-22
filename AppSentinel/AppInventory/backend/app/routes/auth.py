from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    get_jwt_identity, 
    jwt_required,
    get_jwt,
    get_current_user
)
from app.models.user import User
from app import db
from app.utils.logger import logger
import logging
import traceback

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Expose-Headers', 'Authorization')
    return response

@bp.route('/login', methods=['OPTIONS'])
def handle_login_preflight():
    return jsonify({}), 200

@bp.route('/login', methods=['POST'])
def login():
    try:
        print("Starting login attempt")
        logger.debug("Starting login attempt")
        # Get login data
        data = request.get_json()
        print(f"Received request data: {data}")
        logger.debug(f"Received request data: {data}")
        
        username = data.get('username')
        password = data.get('password')
        
        print(f"[POST /auth/login] Login attempt for username: {username}")
        logger.debug(f"[POST /auth/login] Login attempt for username: {username}")
        print(f"[POST /auth/login] Raw request data: {data}")
        logger.debug(f"[POST /auth/login] Raw request data: {data}")
        
        # Validate input
        if not username or not password:
            print("[POST /auth/login] Missing username or password")
            logger.warning("[POST /auth/login] Missing username or password")
            return jsonify({"message": "Missing username or password"}), 400
            
        # For debugging: print all users
        print("Querying all users from database")
        logger.debug("Querying all users from database")
        all_users = User.query.all()
        print(f"[POST /auth/login] All users in database: {[user.username for user in all_users]}")
        logger.debug(f"[POST /auth/login] All users in database: {[user.username for user in all_users]}")
        print(f"[POST /auth/login] All user details: {[(user.username, user.password_hash) for user in all_users]}")
        logger.debug(f"[POST /auth/login] All user details: {[(user.username, user.password_hash) for user in all_users]}")
        
        # Find user
        print(f"Looking up user: {username}")
        logger.debug(f"Looking up user: {username}")
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"[POST /auth/login] User not found: {username}")
            logger.warning(f"[POST /auth/login] User not found: {username}")
            return jsonify({"message": "Invalid username or password"}), 401
            
        print(f"[POST /auth/login] Found user: {user.username}")
        logger.debug(f"[POST /auth/login] Found user: {user.username}")
        print(f"[POST /auth/login] User details: username={user.username}, email={user.email}, role={user.role}, hash={user.password_hash}")
        logger.debug(f"[POST /auth/login] User details: username={user.username}, email={user.email}, role={user.role}, hash={user.password_hash}")
        
        # Check password
        print(f"Checking password for user: {username}")
        logger.debug(f"Checking password for user: {username}")
        if not user.check_password(password):
            print(f"[POST /auth/login] Invalid password for user: {username}")
            logger.warning(f"[POST /auth/login] Invalid password for user: {username}")
            return jsonify({"message": "Invalid username or password"}), 401
            
        # Create access token
        try:
            print(f"Creating access token for user: {username}")
            logger.debug(f"Creating access token for user: {username}")
            access_token = create_access_token(identity=user.id)
            print(f"[POST /auth/login] Created access token for user: {username}")
            logger.debug(f"[POST /auth/login] Created access token for user: {username}")
            logger.debug(f"[POST /auth/login] Token: {access_token}")
        except Exception as e:
            print(f"[POST /auth/login] Error creating access token: {str(e)}")
            logger.error(f"[POST /auth/login] Error creating access token: {str(e)}")
            return jsonify({"message": "Error creating access token"}), 500
            
        # Create refresh token
        try:
            print(f"Creating refresh token for user: {username}")
            logger.debug(f"Creating refresh token for user: {username}")
            refresh_token = create_refresh_token(identity=user.id)
            print(f"[POST /auth/login] Created refresh token for user: {username}")
            logger.debug(f"[POST /auth/login] Created refresh token for user: {username}")
            logger.debug(f"[POST /auth/login] Refresh token: {refresh_token}")
        except Exception as e:
            print(f"[POST /auth/login] Error creating refresh token: {str(e)}")
            logger.error(f"[POST /auth/login] Error creating refresh token: {str(e)}")
            return jsonify({"message": "Error creating refresh token"}), 500
            
        # Return success response
        print(f"[POST /auth/login] Login successful for user: {username}")
        logger.info(f"[POST /auth/login] Login successful for user: {username}")
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
            
    except Exception as e:
        print(f"[POST /auth/login] Unexpected error: {str(e)}")
        logger.error(f"[POST /auth/login] Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"message": "An unexpected error occurred"}), 500

@bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        return jsonify({"message": "Error verifying token"}), 500

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role', 'user')  # Default to 'user' if not specified
        
        if not all([username, password, email]):
            print("[POST /auth/register] All fields are required")
            logger.warning("[POST /auth/register] All fields are required")
            return jsonify({'message': 'All fields are required'}), 400
            
        user = User.query.filter_by(username=username).first()
        if user:
            print("[POST /auth/register] User already exists")
            logger.warning("[POST /auth/register] User already exists")
            return jsonify({'message': 'User already exists'}), 400
            
        user = User(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }), 201
        
    except Exception as e:
        print(f"[POST /auth/register] Error: {str(e)}")
        logger.error(f"[POST /auth/register] Error: {str(e)}")
        db.session.rollback()
        return jsonify({'message': 'Error registering user'}), 500

@bp.route('/user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return jsonify({"message": "Error getting current user"}), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Client should handle token deletion
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify({"message": "Error during logout"}), 500

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }), 200
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        return jsonify({"message": "Error refreshing token"}), 500
