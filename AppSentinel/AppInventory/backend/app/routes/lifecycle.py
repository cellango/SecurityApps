from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.application import Application
from app.models.security_control import SecurityControl, ControlFamily
from app.utils.logger import logger
from sqlalchemy import func

bp = Blueprint('lifecycle', __name__, url_prefix='/api/lifecycle')

@bp.route('/states', methods=['GET'])
@jwt_required()
def get_lifecycle_states():
    """Get all application lifecycle states with statistics"""
    try:
        # Single query to get states, counts, and average scores
        states_data = db.session.query(
            Application.state,
            func.count(Application.id).label('count'),
            func.avg(Application.test_score).label('avg_score')
        ).group_by(Application.state).all()
        
        result = [{
            'state': state.value if hasattr(state, 'value') else state,
            'applicationCount': count,
            'averageSecurityScore': round(float(avg_score or 0), 2),
            'description': get_state_description(state)
        } for state, count, avg_score in states_data]
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in get_lifecycle_states: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/states/<state>/controls', methods=['GET'])
@jwt_required()
def get_state_controls(state):
    """Get all security controls for a specific lifecycle state"""
    try:
        # Get all controls that have this state in their applicable_states (case insensitive)
        controls = SecurityControl.query.filter(
            SecurityControl.applicable_states.ilike(f'%{state}%')
        ).all()
        
        result = []
        for control in controls:
            result.append({
                'id': control.id,
                'controlId': control.control_id,
                'title': control.title,
                'family': control.family.value,
                'description': control.description,
                'applicableStates': control.applicable_states
            })
        
        return jsonify(result)
    except Exception as e:
        logger.error("Error fetching controls for state %s: %s", state, str(e))
        return jsonify({'error': f'Failed to fetch controls for state {state}'}), 500

@bp.route('/controls', methods=['GET'])
@jwt_required()
def get_all_controls():
    """Get all application security controls with statistics"""
    try:
        # Get overall control statistics
        total_controls = SecurityControl.query.count()
        
        # Get controls by family
        controls_by_family = SecurityControl.query.with_entities(
            SecurityControl.family,
            func.count(SecurityControl.id)
        ).group_by(SecurityControl.family).all()
        
        # Format the results
        result = {
            'totalControls': total_controls,
            'controlsByFamily': {
                family.value: count for family, count in controls_by_family
            },
            'families': [family.value for family in ControlFamily]
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error("Error fetching security controls: %s", str(e))
        return jsonify({'error': 'Failed to fetch security controls'}), 500

def get_state_description(state):
    """Return description for each lifecycle state"""
    descriptions = {
        'development': 'Application is in active development',
        'testing': 'Application is undergoing testing',
        'staging': 'Application is in staging environment',
        'production': 'Application is in production',
        'maintenance': 'Application is in maintenance mode',
        'deprecated': 'Application is deprecated',
        'decommissioned': 'Application has been decommissioned'
    }
    return descriptions.get(state, 'No description available')
