from flask import Blueprint, jsonify, request, send_file, current_app
from .models import Application, ApplicationState, SecurityControl, ControlStatus, ControlFamily, ExportFilterPreset, AuditLog
from . import db
from datetime import datetime
from sqlalchemy import func
import pandas as pd
import io
import csv
from sqlalchemy import distinct
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.before_request
def log_request_info():
    logger.debug('Headers: %s', dict(request.headers))
    logger.debug('Body: %s', request.get_data())
    logger.debug('URL: %s', request.url)
    logger.debug('Method: %s', request.method)

@bp.after_request
def log_response_info(response):
    logger.debug('Response Status: %s', response.status)
    logger.debug('Response Headers: %s', dict(response.headers))
    logger.debug('Response Body: %s', response.get_data())
    return response

@bp.route('/applications', methods=['GET'])
def list_applications():
    try:
        logger.debug("Received request for list_applications")
        
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        #logger.debug(f"Page: {page}, Per page: {per_page}")
        
        # Get query parameters for filtering
        department = request.args.get('department')
        team = request.args.get('team')
        
        # Build query
        query = Application.query
        
        # Apply filters
        if department:
            #logger.debug(f"Filtering by department: {department}")
            query = query.filter(Application.department_name == department)
        if team:
            logger.debug(f"Filtering by team: {team}")
            query = query.filter(Application.team_name == team)
            
        # Get total count before pagination
        total_count = query.count()
        logger.debug(f"Total applications in database: {total_count}")
        
        # List all applications for debugging
        all_apps = query.all()
        logger.debug("All applications:")
        for app in all_apps:
            logger.debug(f"ID: {app.id}, Name: {app.name}, Department: {app.department_name}, Team: {app.team_name}")
        
        # Get paginated applications
        applications = query.paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )
        
        # Convert to list of dicts
        result = {
            'items': [{
                'id': app.id,
                'name': app.name,
                'description': app.description,
                'application_type': app.application_type.value,
                'state': app.state.value,
                'owner_id': app.owner_id,
                'owner_email': app.owner_email,
                'department_name': app.department_name,
                'team_name': app.team_name,
                'test_score': app.test_score,
                'data_classification': app.data_classification,
                'authentication_method': app.authentication_method,
                'requires_2fa': app.requires_2fa
            } for app in applications.items],
            'total': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
        
        logger.debug(f"Returning {len(result['items'])} applications")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in list_applications: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    try:
        logger.debug(f'Received request for application {app_id}')
        
        app = Application.query.get_or_404(app_id)
        
        result = {
            'id': app.id,
            'name': app.name,
            'description': app.description,
            'application_type': app.application_type.value,
            'state': app.state.value,
            'owner_id': app.owner_id,
            'owner_email': app.owner_email,
            'department_name': app.department_name,
            'team_name': app.team_name,
            'test_score': app.test_score,
            'test_score_date': app.test_score_date.isoformat() if app.test_score_date else None,
            'last_security_review': app.last_security_review.isoformat() if app.last_security_review else None,
            'next_security_review': app.next_security_review.isoformat() if app.next_security_review else None,
            'deployment_date': app.deployment_date.isoformat() if app.deployment_date else None,
            'last_update_date': app.last_update_date.isoformat() if app.last_update_date else None,
            'vendor_name': app.vendor_name,
            'vendor_contact': app.vendor_contact,
            'contract_expiration': app.contract_expiration.isoformat() if app.contract_expiration else None,
            'data_classification': app.data_classification,
            'authentication_method': app.authentication_method,
            'requires_2fa': app.requires_2fa,
            'controls': [{
                'id': ac.control.id,
                'control_id': ac.control.control_id,
                'family': ac.control.family.value,
                'title': ac.control.title,
                'description': ac.control.description,
                'status': ac.status.value,
                'implementation_date': ac.implementation_date.isoformat() if ac.implementation_date else None,
                'last_review_date': ac.last_review_date.isoformat() if ac.last_review_date else None,
                'notes': ac.notes
            } for ac in app.application_controls]
        }
        
        logger.debug('Response Status: 200 OK')
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_application: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/<int:app_id>/controls', methods=['GET'])
def get_application_controls(app_id):
    try:
        logger.debug(f'Received request for application {app_id} controls')
        
        app = Application.query.get_or_404(app_id)
        
        result = [{
            'id': ac.control.id,
            'control_id': ac.control.control_id,
            'family': ac.control.family.value,
            'title': ac.control.title,
            'description': ac.control.description,
            'status': ac.status.value,
            'implementation_date': ac.implementation_date.isoformat() if ac.implementation_date else None,
            'last_review_date': ac.last_review_date.isoformat() if ac.last_review_date else None,
            'notes': ac.notes
        } for ac in app.application_controls]
        
        logger.debug('Response Status: 200 OK')
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_application_controls: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/controls', methods=['GET'])
def get_controls_dashboard():
    try:
        logger.debug('Received request for controls dashboard')
        
        # Get overall statistics
        total_controls = db.session.query(func.count(SecurityControl.id)).scalar()
        total_applications = db.session.query(func.count(Application.id)).scalar()
        
        # Get implementation status across all applications
        status_stats = db.session.query(
            ControlStatus,
            func.count(ApplicationControl.status)
        ).select_from(ApplicationControl).group_by(
            ApplicationControl.status
        ).all()
        
        # Get statistics by control family
        family_stats = db.session.query(
            SecurityControl.family,
            func.count(SecurityControl.id)
        ).group_by(SecurityControl.family).all()
        
        # Get implementation progress by application
        app_progress = db.session.query(
            Application.id,
            Application.name,
            func.count(ApplicationControl.control_id).label('implemented'),
            func.count(SecurityControl.id).label('total')
        ).join(
            ApplicationControl, Application.id == ApplicationControl.application_id, isouter=True
        ).join(
            SecurityControl, SecurityControl.id == ApplicationControl.control_id, isouter=True
        ).group_by(Application.id, Application.name).all()
        
        result = {
            'summary': {
                'total_controls': total_controls,
                'total_applications': total_applications,
                'status_distribution': {
                    status.value: count for status, count in status_stats
                }
            },
            'family_distribution': {
                family.value: count for family, count in family_stats
            },
            'application_progress': [{
                'id': app_id,
                'name': name,
                'implemented': implemented,
                'total': total,
                'percentage': (implemented / total * 100) if total > 0 else 0
            } for app_id, name, implemented, total in app_progress]
        }
        
        logger.debug('Response Status: 200 OK')
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_controls_dashboard: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/<int:app_id>/controls/<int:control_id>', methods=['PUT'])
def update_control_status(app_id, control_id):
    try:
        logger.debug(f'Received request for update control status for application {app_id} and control {control_id}')
        
        app = Application.query.get_or_404(app_id)
        control = SecurityControl.query.get_or_404(control_id)
        
        data = request.json
        status = data.get('status')
        notes = data.get('notes')
        
        if not status:
            return jsonify({'error': 'Status is required'}), 400
        
        try:
            status_enum = ControlStatus[status.upper()]
        except KeyError:
            return jsonify({'error': 'Invalid status provided'}), 400
        
        # Update or create the control status
        application_control = next((ac for ac in app.application_controls 
                                  if ac.control_id == control_id), None)
        
        if application_control:
            application_control.status = status_enum
            application_control.notes = notes
            application_control.last_review_date = datetime.utcnow()
        else:
            app.application_controls.append({
                'control_id': control_id,
                'status': status_enum,
                'notes': notes,
                'implementation_date': datetime.utcnow() if status_enum == ControlStatus.IMPLEMENTED else None,
                'last_review_date': datetime.utcnow()
            })
        
        db.session.commit()
        return jsonify({'message': 'Control status updated successfully'})
        
    except Exception as e:
        logger.error(f'Error in update_control_status: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/applications', methods=['POST'])
def create_application():
    try:
        data = request.get_json()
        
        # Get audit context from request headers
        user_id = request.headers.get('X-User-ID')
        jira_ticket = request.headers.get('X-Jira-Ticket')
        
        application = Application(
            name=data['name'],
            description=data.get('description'),
            application_type=data['application_type'],
            state=data['state'],
            owner_id=data['owner_id'],
            owner_email=data['owner_email'],
            department_name=data['department_name'],
            team_name=data['team_name'],
            data_classification=data.get('data_classification'),
            authentication_method=data.get('authentication_method'),
            requires_2fa=data.get('requires_2fa', False),
            test_score=data.get('test_score')
        )
        
        # Set audit context
        application._audit_user_id = user_id
        application._audit_jira_ticket = jira_ticket
        application.created_by = user_id
        application.updated_by = user_id
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({"message": "Application created successfully", "id": application.id}), 201
        
    except Exception as e:
        logger.error(f"Error in create_application: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/<int:id>', methods=['PUT'])
def update_application(id):
    try:
        application = Application.query.get_or_404(id)
        data = request.get_json()
        
        # Get audit context from request headers
        user_id = request.headers.get('X-User-ID')
        jira_ticket = request.headers.get('X-Jira-Ticket')
        
        # Set audit context
        application._audit_user_id = user_id
        application._audit_jira_ticket = jira_ticket
        application.updated_by = user_id
        
        # Update fields
        if 'name' in data:
            application.name = data['name']
        if 'description' in data:
            application.description = data['description']
        if 'application_type' in data:
            application.application_type = data['application_type']
        if 'state' in data:
            application.state = data['state']
        if 'owner_id' in data:
            application.owner_id = data['owner_id']
        if 'owner_email' in data:
            application.owner_email = data['owner_email']
        if 'department_name' in data:
            application.department_name = data['department_name']
        if 'team_name' in data:
            application.team_name = data['team_name']
        if 'data_classification' in data:
            application.data_classification = data['data_classification']
        if 'authentication_method' in data:
            application.authentication_method = data['authentication_method']
        if 'requires_2fa' in data:
            application.requires_2fa = data['requires_2fa']
        if 'test_score' in data:
            application.test_score = data['test_score']
        
        db.session.commit()
        return jsonify({"message": "Application updated successfully"})
        
    except Exception as e:
        logger.error(f"Error in update_application: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    try:
        application = Application.query.get_or_404(id)
        
        # Get audit context from request headers
        user_id = request.headers.get('X-User-ID')
        jira_ticket = request.headers.get('X-Jira-Ticket')
        
        # Set audit context
        application._audit_user_id = user_id
        application._audit_jira_ticket = jira_ticket
        
        db.session.delete(application)
        db.session.commit()
        return jsonify({"message": "Application deleted successfully"})
        
    except Exception as e:
        logger.error(f"Error in delete_application: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/controls/export', methods=['GET'])
def export_controls_dashboard():
    try:
        logger.debug('Received request for export controls dashboard')
        
        export_format = request.args.get('format', 'csv')
        
        # Get filter parameters
        department = request.args.get('department')
        team = request.args.get('team')
        control_family = request.args.get('family')
        status = request.args.get('status')
        implementation_date_start = request.args.get('implementation_date_start')
        implementation_date_end = request.args.get('implementation_date_end')
        
        # Build the query
        query = db.session.query(Application, SecurityControl, ApplicationControl).\
            join(ApplicationControl, Application.id == ApplicationControl.application_id, isouter=True).\
            join(SecurityControl, SecurityControl.id == ApplicationControl.control_id, isouter=True)
        
        # Apply filters
        if department:
            query = query.filter(Application.department_name == department)
        if team:
            query = query.filter(Application.team_name == team)
        if control_family:
            try:
                family_enum = ControlFamily[control_family.upper()]
                query = query.filter(SecurityControl.family == family_enum)
            except KeyError:
                return jsonify({'error': 'Invalid control family'}), 400
        if status:
            try:
                status_enum = ControlStatus[status.upper()]
                query = query.filter(ApplicationControl.status == status_enum)
            except KeyError:
                return jsonify({'error': 'Invalid status'}), 400
        if implementation_date_start:
            try:
                start_date = datetime.strptime(implementation_date_start, '%Y-%m-%d')
                query = query.filter(ApplicationControl.implementation_date >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start date format'}), 400
        if implementation_date_end:
            try:
                end_date = datetime.strptime(implementation_date_end, '%Y-%m-%d')
                query = query.filter(ApplicationControl.implementation_date <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end date format'}), 400
        
        # Execute query
        results = query.all()
        
        # Prepare data for export
        export_data = []
        for app, control, implementation in results:
            export_data.append({
                'Application Name': app.name,
                'Application State': app.state.value,
                'Department': app.department_name,
                'Team': app.team_name,
                'Control ID': control.control_id,
                'Control Family': control.family.value,
                'Control Title': control.title,
                'Implementation Status': implementation.status.value if implementation else 'Not Implemented',
                'Implementation Date': implementation.implementation_date.strftime('%Y-%m-%d') if implementation and implementation.implementation_date else '',
                'Last Review Date': implementation.last_review_date.strftime('%Y-%m-%d') if implementation and implementation.last_review_date else '',
                'Notes': implementation.notes if implementation else ''
            })
        
        if not export_data:
            return jsonify({'error': 'No data found matching the specified filters'}), 404
        
        if export_format == 'csv':
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)
            
            # Create the CSV in memory
            mem_file = io.BytesIO()
            mem_file.write(output.getvalue().encode('utf-8'))
            mem_file.seek(0)
            output.close()
            
            return send_file(
                mem_file,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'security_controls_export_{datetime.now().strftime("%Y%m%d")}.csv'
            )
        
        elif export_format == 'excel':
            df = pd.DataFrame(export_data)
            
            # Create Excel file in memory
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # Write main data
                df.to_excel(writer, sheet_name='Controls Implementation', index=False)
                
                # Create summary sheet with filter information
                summary_data = {
                    'Metric': [
                        'Total Applications',
                        'Total Controls',
                        'Implemented Controls',
                        'Partially Implemented Controls',
                        'Planned Controls',
                        'Not Implemented Controls',
                        '',
                        'Applied Filters:',
                        'Department',
                        'Team',
                        'Control Family',
                        'Status',
                        'Implementation Date Range'
                    ],
                    'Value': [
                        len(set(d['Application Name'] for d in export_data)),
                        len(set(d['Control ID'] for d in export_data)),
                        len([d for d in export_data if d['Implementation Status'] == 'implemented']),
                        len([d for d in export_data if d['Implementation Status'] == 'partially_implemented']),
                        len([d for d in export_data if d['Implementation Status'] == 'planned']),
                        len([d for d in export_data if d['Implementation Status'] == 'not_implemented']),
                        '',
                        '',
                        department or 'All',
                        team or 'All',
                        control_family or 'All',
                        status or 'All',
                        f"{implementation_date_start or 'Any'} to {implementation_date_end or 'Any'}"
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Create family distribution sheet
                family_dist = df.groupby('Control Family').size().reset_index(name='Count')
                family_dist.to_excel(writer, sheet_name='Family Distribution', index=False)
                
                # Create application progress sheet
                app_progress = df.groupby('Application Name').agg({
                    'Control ID': 'count',
                    'Implementation Status': lambda x: (x == 'implemented').sum()
                }).reset_index()
                app_progress.columns = ['Application Name', 'Total Controls', 'Implemented Controls']
                app_progress['Implementation Percentage'] = (
                    app_progress['Implemented Controls'] / app_progress['Total Controls'] * 100
                ).round(2)
                app_progress.to_excel(writer, sheet_name='Application Progress', index=False)
            
            excel_file.seek(0)
            
            return send_file(
                excel_file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'security_controls_export_{datetime.now().strftime("%Y%m%d")}.xlsx'
            )
        
        return jsonify({'error': 'Invalid export format'}), 400
        
    except Exception as e:
        logger.error(f'Error in export_controls_dashboard: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/filter-suggestions', methods=['GET'])
def get_filter_suggestions():
    try:
        logger.debug('Received request for filter suggestions')
        
        departments = db.session.query(Application.department_name).distinct().all()
        teams = db.session.query(Application.team_name).distinct().all()
        
        result = {
            'departments': [dept[0] for dept in departments if dept[0]],
            'teams': [team[0] for team in teams if team[0]]
        }
        logger.debug('Filter suggestions: %s', result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_filter_suggestions: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/filters/suggestions', methods=['GET'])
def get_dashboard_filter_suggestions():
    try:
        logger.debug('Received request for dashboard filter suggestions')
        
        # Get unique departments
        departments = db.session.query(distinct(Application.department_name)).\
            filter(Application.department_name.isnot(None)).all()
        
        # Get unique teams
        teams = db.session.query(distinct(Application.team_name)).\
            filter(Application.team_name.isnot(None)).all()
        
        # Get implementation date ranges
        date_range = db.session.query(
            func.min(ApplicationControl.implementation_date).label('min_date'),
            func.max(ApplicationControl.implementation_date).label('max_date')
        ).first()
        
        result = {
            'departments': [d[0] for d in departments],
            'teams': [t[0] for t in teams],
            'control_families': [f.value for f in ControlFamily],
            'statuses': [s.value for s in ControlStatus],
            'implementation_date_range': {
                'min': date_range.min_date.isoformat() if date_range.min_date else None,
                'max': date_range.max_date.isoformat() if date_range.max_date else None
            }
        }
        logger.debug('Dashboard filter suggestions: %s', result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_dashboard_filter_suggestions: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/filters/presets', methods=['GET'])
def get_filter_presets():
    try:
        logger.debug('Received request for filter presets')
        
        presets = ExportFilterPreset.query.order_by(
            ExportFilterPreset.last_used.desc()
        ).all()
        
        result = [{
            'id': preset.id,
            'name': preset.name,
            'department': preset.department,
            'team': preset.team,
            'control_family': preset.control_family.value if preset.control_family else None,
            'status': preset.status.value if preset.status else None,
            'implementation_date_start': preset.implementation_date_start.isoformat() if preset.implementation_date_start else None,
            'implementation_date_end': preset.implementation_date_end.isoformat() if preset.implementation_date_end else None,
            'created_at': preset.created_at.isoformat(),
            'last_used': preset.last_used.isoformat() if preset.last_used else None
        } for preset in presets]
        logger.debug('Filter presets: %s', result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in get_filter_presets: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/filters/presets', methods=['POST'])
def create_filter_preset():
    try:
        logger.debug('Received request for create filter preset')
        
        data = request.json
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Preset name is required'}), 400
            
        # Create new preset
        preset = ExportFilterPreset(
            name=data['name'],
            department=data.get('department'),
            team=data.get('team'),
            control_family=ControlFamily[data['control_family'].upper()] if data.get('control_family') else None,
            status=ControlStatus[data['status'].upper()] if data.get('status') else None,
            implementation_date_start=datetime.strptime(data['implementation_date_start'], '%Y-%m-%d') if data.get('implementation_date_start') else None,
            implementation_date_end=datetime.strptime(data['implementation_date_end'], '%Y-%m-%d') if data.get('implementation_date_end') else None,
            last_used=datetime.utcnow()
        )
        
        db.session.add(preset)
        db.session.commit()
        
        result = {
            'id': preset.id,
            'name': preset.name,
            'created_at': preset.created_at.isoformat()
        }
        logger.debug('Created filter preset: %s', result)
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f'Error in create_filter_preset: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/filters/presets/<int:preset_id>', methods=['DELETE'])
def delete_filter_preset(preset_id):
    try:
        logger.debug(f'Received request for delete filter preset {preset_id}')
        
        preset = ExportFilterPreset.query.get_or_404(preset_id)
        db.session.delete(preset)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        logger.error(f'Error in delete_filter_preset: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/dashboard/filters/presets/<int:preset_id>/use', methods=['POST'])
def use_filter_preset(preset_id):
    try:
        logger.debug(f'Received request for use filter preset {preset_id}')
        
        preset = ExportFilterPreset.query.get_or_404(preset_id)
        preset.last_used = datetime.utcnow()
        db.session.commit()
        
        result = {
            'id': preset.id,
            'last_used': preset.last_used.isoformat()
        }
        logger.debug('Updated filter preset: %s', result)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in use_filter_preset: {str(e)}')
        return jsonify({"error": str(e)}), 500

@bp.route('/applications/search', methods=['GET'])
def search_applications():
    try:
        logger.debug("Received request for search_applications")
        logger.debug(f"Request headers: {dict(request.headers)}")
        logger.debug(f"Query params: {dict(request.args)}")
        
        query = request.args.get('q', '').strip()
        logger.debug(f"Search query: {query}")
        
        if not query:
            logger.debug("Empty query, returning empty list")
            return jsonify([])
            
        # Escape special characters in the search query
        query = query.replace('%', r'\%').replace('_', r'\_')
        
        # Use ilike for case-insensitive search with wildcards
        search_query = Application.query.filter(
            db.or_(
                Application.name.ilike(f'%{query}%'),
                Application.description.ilike(f'%{query}%'),
                Application.department_name.ilike(f'%{query}%'),
                Application.team_name.ilike(f'%{query}%')
            )
        ).order_by(Application.name.asc())  # Sort results alphabetically
        
        logger.debug(f"SQL Query: {str(search_query)}")
        
        applications = search_query.all()
        logger.debug(f"Found {len(applications)} matching applications")
        
        result = [{
            'id': app.id,
            'name': app.name,
            'description': app.description,
            'application_type': app.application_type,
            'state': app.state,
            'department_name': app.department_name,
            'team_name': app.team_name
        } for app in applications]
        
        logger.debug(f"Response payload: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in search_applications: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500

@bp.route('/audit-logs', methods=['GET'])
def list_audit_logs():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        table_name = request.args.get('table_name')
        record_id = request.args.get('record_id', type=int)
        action = request.args.get('action')
        user_id = request.args.get('user_id')
        jira_ticket = request.args.get('jira_ticket')
        
        # Build query
        query = AuditLog.query
        
        # Apply filters
        if table_name:
            query = query.filter(AuditLog.table_name == table_name)
        if record_id:
            query = query.filter(AuditLog.record_id == record_id)
        if action:
            query = query.filter(AuditLog.action == action)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if jira_ticket:
            query = query.filter(AuditLog.jira_ticket == jira_ticket)
        
        # Order by timestamp descending
        query = query.order_by(AuditLog.timestamp.desc())
        
        # Paginate results
        audit_logs = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Convert to response format
        result = {
            'items': [{
                'id': log.id,
                'table_name': log.table_name,
                'record_id': log.record_id,
                'action': log.action,
                'changed_fields': log.changed_fields,
                'user_id': log.user_id,
                'jira_ticket': log.jira_ticket,
                'timestamp': log.timestamp.isoformat()
            } for log in audit_logs.items],
            'total': audit_logs.total,
            'page': page,
            'per_page': per_page,
            'total_pages': (audit_logs.total + per_page - 1) // per_page
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in list_audit_logs: {str(e)}")
        logger.exception("Full traceback:")
        return jsonify({"error": str(e)}), 500
