"""
Routes package initialization.
"""
from flask import Blueprint

# Create the main blueprint
bp = Blueprint('main', __name__, url_prefix='/api')

def init_app(app):
    """Initialize application routes."""
    from . import auth, dashboard, lifecycle, applications, departments
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(lifecycle.bp)
    app.register_blueprint(applications.bp)
    app.register_blueprint(departments.bp)
