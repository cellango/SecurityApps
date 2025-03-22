from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.application import Application
from app.models.user import User
from app import db
from app.utils.logger import logger
from sqlalchemy import or_

bp = Blueprint('applications', __name__, url_prefix='/api/applications')

@bp.route('', methods=['GET'])
@jwt_required()
def get_applications():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search_query = request.args.get('q', '')
        department = request.args.get('department', '')
        team = request.args.get('team', '')

        # Start with base query
        query = Application.query

        # Apply search filter if provided
        if search_query:
            search_filter = or_(
                Application.name.ilike(f'%{search_query}%'),
                Application.description.ilike(f'%{search_query}%')
            )
            query = query.filter(search_filter)

        # Apply department filter if provided
        if department:
            query = query.filter(Application.department_name == department)

        # Apply team filter if provided
        if team:
            query = query.filter(Application.team_name == team)

        # Get paginated results
        paginated_apps = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'applications': [app.to_dict() for app in paginated_apps.items],
            'total': paginated_apps.total,
            'page': page,
            'per_page': per_page,
            'pages': paginated_apps.pages
        }), 200
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}")
        return jsonify({'message': 'Error fetching applications'}), 500

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
        return jsonify(application.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching application {id}: {str(e)}")
        return jsonify({'message': 'Error fetching application'}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_application():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        required_fields = ['name', 'description', 'application_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        application = Application(
            name=data['name'],
            description=data['description'],
            application_type=data['application_type'],
            owner_id=get_jwt_identity()
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify(application.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating application: {str(e)}")
        return jsonify({'message': 'Error creating application'}), 500

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        # Update fields
        for field in ['name', 'description', 'application_type', 'state']:
            if field in data:
                setattr(application, field, data[field])
        
        db.session.commit()
        return jsonify(application.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating application {id}: {str(e)}")
        return jsonify({'message': 'Error updating application'}), 500

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_application(id):
    try:
        application = Application.query.get(id)
        if not application:
            return jsonify({'message': 'Application not found'}), 404
            
        db.session.delete(application)
        db.session.commit()
        return jsonify({'message': 'Application deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting application {id}: {str(e)}")
        return jsonify({'message': 'Error deleting application'}), 500

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_applications():
    """Search for applications by name, description, department, or team"""
    try:
        logger.info("[GET /search] Request received")
        logger.info("[GET /search] Headers: %s", dict(request.headers))
        logger.info("[GET /search] Args: %s", dict(request.args))
        
        search_term = request.args.get('q', '').strip()
        logger.info("[GET /search] Search term: %s", search_term)
        
        if not search_term:
            logger.info("[GET /search] Empty search term, returning empty list")
            return jsonify([]), 200

        # Escape special characters in the search query
        search_term = search_term.replace('%', r'\%').replace('_', r'\_')
        
        # Case-insensitive search using ILIKE across multiple fields
        applications = Application.query.filter(
            or_(
                Application.name.ilike(f'%{search_term}%'),
                Application.description.ilike(f'%{search_term}%'),
                Application.department_name.ilike(f'%{search_term}%'),
                Application.team_name.ilike(f'%{search_term}%')
            )
        ).order_by(Application.name.asc()).limit(10).all()

        logger.info("[GET /search] Found %d matching applications", len(applications))
        
        result = []
        for app in applications:
            app_data = {
                'id': app.id,
                'name': app.name,
                'description': app.description or '',
                'department_name': app.department_name or '',
                'team_name': app.team_name or '',
                'application_type': app.application_type or ''
            }
            result.append(app_data)
            logger.info("[GET /search] Adding application: %s", app_data)

        logger.info("[GET /search] Returning %d results", len(result))
        return jsonify(result), 200

    except Exception as e:
        logger.error("[GET /search] Error: %s", str(e))
        logger.exception("[GET /search] Full traceback:")
        return jsonify({"message": "Error searching applications", "error": str(e)}), 500
