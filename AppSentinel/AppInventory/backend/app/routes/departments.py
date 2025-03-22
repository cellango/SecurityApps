from flask import Blueprint, jsonify, request, current_app
from app.models.department import Department
from app.models.team import Team
from app.models.application import Application
from app import db
from app.utils.logger import logger
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback

bp = Blueprint('departments', __name__, url_prefix='/api')

@bp.route('/departments', methods=['GET', 'OPTIONS'])
def get_departments():
    """Get all departments"""
    if request.method == 'OPTIONS':
        return '', 200
        
    @jwt_required()
    def get():
        try:
            # Log request info
            current_user = get_jwt_identity()
            logger.info(f"[GET /departments] Request received from user: {current_user}")
            
            # Debug: print request headers
            logger.debug(f"[GET /departments] Request headers: {dict(request.headers)}")
            logger.debug(f"[GET /departments] Authorization header: {request.headers.get('Authorization')}")
            
            # Query departments
            logger.info("[GET /departments] Querying departments from database")
            departments = Department.query.all()
            
            # Debug: print raw departments
            logger.info(f"[GET /departments] Raw departments: {departments}")
            for dept in departments:
                logger.info(f"[GET /departments] Department: id={dept.id}, name={dept.name}")
            
            logger.info(f"[GET /departments] Found {len(departments) if departments else 0} departments")
            
            if not departments:
                logger.warning("[GET /departments] No departments found in database")
                return jsonify([]), 200
            
            # Convert to dict
            logger.info("[GET /departments] Converting departments to dict")
            result = []
            for dept in departments:
                try:
                    dept_dict = dept.to_dict()
                    logger.debug(f"[GET /departments] Converted department: {dept_dict}")
                    result.append(dept_dict)
                except Exception as e:
                    logger.error(f"[GET /departments] Error converting department {dept.id}: {str(e)}")
                    logger.error(traceback.format_exc())
                    continue
            
            logger.info(f"[GET /departments] Successfully returning {len(result)} departments")
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"[GET /departments] Error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"message": "An error occurred while fetching departments"}), 500
            
    return get()

@bp.route('/departments/<int:department_id>/teams', methods=['GET'])
@jwt_required()
def get_department_teams(department_id):
    """Get all teams for a specific department"""
    try:
        # Log request info
        current_user = get_jwt_identity()
        logger.info(f"[GET /departments/{department_id}/teams] Request received from user: {current_user}")
        
        # Query department
        department = Department.query.get(department_id)
        if not department:
            logger.warning(f"[GET /departments/{department_id}/teams] Department not found")
            return jsonify({"message": "Department not found"}), 404
        
        # Query teams
        teams = department.teams.all()
        
        # Convert to dict
        result = []
        for team in teams:
            try:
                team_dict = team.to_dict()
                result.append(team_dict)
            except Exception as e:
                logger.error(f"[GET /departments/{department_id}/teams] Error converting team {team.id}: {str(e)}")
                continue
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"[GET /departments/{department_id}/teams] Error: {str(e)}")
        return jsonify({"message": str(e)}), 500

@bp.route('/teams/<int:team_id>/applications', methods=['GET'])
@jwt_required()
def get_team_applications(team_id):
    """Get all applications for a specific team"""
    try:
        # Log request info
        current_user = get_jwt_identity()
        logger.info(f"[GET /teams/{team_id}/applications] Request received from user: {current_user}")
        
        # Query team
        team = Team.query.get(team_id)
        if not team:
            logger.warning(f"[GET /teams/{team_id}/applications] Team not found")
            return jsonify({"message": "Team not found"}), 404
        
        # Query applications
        applications = team.applications.all()
        
        # Convert to dict
        result = []
        for app in applications:
            try:
                app_dict = app.to_dict()
                result.append(app_dict)
            except Exception as e:
                logger.error(f"[GET /teams/{team_id}/applications] Error converting application {app.id}: {str(e)}")
                continue
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"[GET /teams/{team_id}/applications] Error: {str(e)}")
        return jsonify({"message": str(e)}), 500

@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
