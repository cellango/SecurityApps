from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.application import Application
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.security_control import SecurityControl
from app.utils.logger import logger
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    """Get dashboard data including stats, recent applications, and activity"""
    try:
        # Get applications with their scores and risk levels
        applications = Application.query.order_by(
            Application.created_at.desc()
        ).all()

        # Calculate statistics
        total_apps = len(applications)
        high_risk_apps = sum(1 for app in applications if app.risk_level == 'HIGH')
        
        # Calculate average score
        if total_apps > 0:
            average_score = round(sum(app.security_score for app in applications) / total_apps)
        else:
            average_score = 0

        # Get pending reviews (due within 30 days)
        pending_reviews = Application.query.filter(
            Application.next_review_date <= datetime.utcnow() + timedelta(days=30)
        ).count()

        # Get recent activity
        recent_activity = AuditLog.query.order_by(
            AuditLog.timestamp.desc()
        ).limit(10).all()

        # Format application data
        app_data = [{
            'id': app.id,
            'name': app.name,
            'risk_level': app.risk_level,
            'security_score': app.security_score,
            'last_review_date': app.last_review_date.isoformat() if app.last_review_date else None,
            'next_review_date': app.next_review_date.isoformat() if app.next_review_date else None
        } for app in applications]

        # Format activity data
        activity_data = [{
            'id': log.id,
            'action': log.action,
            'entity_type': log.entity_type,
            'entity_id': log.entity_id,
            'user_id': log.user_id,
            'timestamp': log.timestamp.isoformat()
        } for log in recent_activity]

        return jsonify({
            'stats': {
                'totalApps': total_apps,
                'highRiskApps': high_risk_apps,
                'pendingReviews': pending_reviews,
                'averageScore': average_score
            },
            'recentApplications': app_data,
            'recentActivity': activity_data
        })

    except Exception as e:
        logger.error(f"Error fetching dashboard data", error=str(e))
        return jsonify({
            'error': 'Failed to fetch dashboard data'
        }), 500

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get dashboard statistics"""
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Get applications data
        applications = Application.query.all()
        total_apps = len(applications)
        high_risk_apps = sum(1 for app in applications if app.risk_level == 'HIGH')
        
        # Calculate average score
        if total_apps > 0:
            average_score = round(sum(app.security_score for app in applications) / total_apps)
        else:
            average_score = 0

        # Get pending reviews
        pending_reviews = Application.query.filter(
            Application.next_review_date <= datetime.utcnow() + timedelta(days=30)
        ).count()

        # Get total controls
        total_controls = SecurityControl.query.count()

        return jsonify({
            'totalApps': total_apps,
            'highRiskApps': high_risk_apps,
            'pendingReviews': pending_reviews,
            'averageScore': average_score,
            'totalControls': total_controls,
            'user': user.to_dict()
        })

    except Exception as e:
        logger.error(f"Error fetching dashboard stats", error=str(e))
        return jsonify({
            'error': 'Failed to fetch dashboard statistics'
        }), 500
