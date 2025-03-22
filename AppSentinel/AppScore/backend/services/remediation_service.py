from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.score_history import ScoreHistory

class RemediationService:
    def __init__(self, session: Session):
        self.session = session

    def get_remediations(self, application_id: int) -> List[Dict[str, Any]]:
        """Generate remediation recommendations based on latest score and findings"""
        try:
            # Get latest score history
            latest_score = (
                self.session.query(ScoreHistory)
                .filter_by(application_id=application_id)
                .order_by(ScoreHistory.created_at.desc())
                .first()
            )

            if not latest_score:
                return []

            remediations = []
            features = latest_score.features

            # Check for critical vulnerabilities
            if features.get('critical_vulns', 0) > 0:
                remediations.append({
                    'title': 'Address Critical Vulnerabilities',
                    'description': f'Found {features["critical_vulns"]} critical vulnerabilities. '
                                 'These should be addressed immediately as they pose significant security risks.',
                    'severity': 'critical',
                    'effort': 'High',
                    'impact': 20
                })

            # Check for high vulnerabilities
            if features.get('high_vulns', 0) > 2:
                remediations.append({
                    'title': 'Fix High-Risk Vulnerabilities',
                    'description': f'Found {features["high_vulns"]} high-risk vulnerabilities. '
                                 'These should be addressed in the next sprint.',
                    'severity': 'high',
                    'effort': 'Medium',
                    'impact': 15
                })

            # Check outdated dependencies
            if features.get('outdated_deps_percentage', 0) > 20:
                remediations.append({
                    'title': 'Update Dependencies',
                    'description': f'{features["outdated_deps_percentage"]}% of dependencies are outdated. '
                                 'Update to latest stable versions to prevent security vulnerabilities.',
                    'severity': 'medium',
                    'effort': 'Medium',
                    'impact': 10
                })

            # Check code coverage
            if features.get('code_coverage', 100) < 80:
                remediations.append({
                    'title': 'Improve Test Coverage',
                    'description': f'Current code coverage is {features["code_coverage"]}%. '
                                 'Increase test coverage to at least 80% to ensure better code quality.',
                    'severity': 'low',
                    'effort': 'High',
                    'impact': 5
                })

            # Check security hotspots
            if features.get('security_hotspots', 0) > 5:
                remediations.append({
                    'title': 'Review Security Hotspots',
                    'description': f'Found {features["security_hotspots"]} security hotspots. '
                                 'Review and fix potential security issues in the codebase.',
                    'severity': 'medium',
                    'effort': 'Medium',
                    'impact': 8
                })

            # Check compliance violations
            if features.get('compliance_violations', 0) > 0:
                remediations.append({
                    'title': 'Address Compliance Issues',
                    'description': f'Found {features["compliance_violations"]} compliance violations. '
                                 'Review and fix to ensure regulatory compliance.',
                    'severity': 'high',
                    'effort': 'High',
                    'impact': 15
                })

            # Sort remediations by impact
            remediations.sort(key=lambda x: x['impact'], reverse=True)
            
            return remediations

        except Exception as e:
            print(f"Error generating remediations: {str(e)}")
            return []

    def get_remediation_progress(self, application_id: int) -> Dict[str, Any]:
        """Get progress on implementing remediations"""
        try:
            # Get historical scores
            scores = (
                self.session.query(ScoreHistory)
                .filter_by(application_id=application_id)
                .order_by(ScoreHistory.created_at.desc())
                .limit(10)
                .all()
            )

            if not scores:
                return {'status': 'No historical data available'}

            latest = scores[0].features
            oldest = scores[-1].features

            improvements = []

            # Check various metrics for improvements
            if latest.get('critical_vulns', 0) < oldest.get('critical_vulns', 0):
                improvements.append({
                    'metric': 'Critical Vulnerabilities',
                    'change': oldest['critical_vulns'] - latest['critical_vulns'],
                    'impact': 'high'
                })

            if latest.get('high_vulns', 0) < oldest.get('high_vulns', 0):
                improvements.append({
                    'metric': 'High Vulnerabilities',
                    'change': oldest['high_vulns'] - latest['high_vulns'],
                    'impact': 'medium'
                })

            if latest.get('code_coverage', 0) > oldest.get('code_coverage', 0):
                improvements.append({
                    'metric': 'Code Coverage',
                    'change': latest['code_coverage'] - oldest['code_coverage'],
                    'impact': 'low'
                })

            return {
                'status': 'Success',
                'improvements': improvements,
                'score_change': latest.get('final_score', 0) - oldest.get('final_score', 0),
                'period': '10 most recent scores'
            }

        except Exception as e:
            print(f"Error getting remediation progress: {str(e)}")
            return {'status': 'Error getting progress'}
