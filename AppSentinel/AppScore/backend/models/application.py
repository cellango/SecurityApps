from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from extensions import db
from enum import Enum

class ApplicationType(str, Enum):
    INTERNAL = 'internal'
    VENDOR = 'vendor'
    WEB = 'web'
    API = 'api'
    MOBILE = 'mobile'
    BUILT = 'built'
    BOUGHT = 'bought'

class Application(db.Model):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    app_type = Column(String(10), nullable=False)
    vendor_name = Column(String(100))
    vendor_contact = Column(String(100))
    support_url = Column(String(200))
    security_score = Column(Float, default=0.0)
    last_scored = Column(DateTime)  
    created_at = Column(DateTime, default=datetime.utcnow)
    team_id = Column(Integer, ForeignKey('teams.id'))
    catalog_id = Column(String(100), unique=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationship to Team
    team = relationship('Team', back_populates='applications')

    # Add relationship to ScoreHistory
    score_history = relationship('ScoreHistory', back_populates='application', cascade='all, delete-orphan')

    @property
    def security_score(self):
        """Get the latest security score for this application"""
        latest_score = next((score for score in sorted(
            self.score_history,
            key=lambda x: x.created_at,
            reverse=True
        )), None)
        return latest_score.score if latest_score else None

    def calculate_risk_score(self, risk_params):
        """Calculate risk score based on application type and risk parameters"""
        if self.app_type == "internal":
            weights = risk_params.internal_weights
            thresholds = risk_params.internal_thresholds
            
            # Example scoring for internal applications
            scores = {
                'code_review': self._calculate_code_review_score(),
                'security_testing': self._calculate_security_testing_score(),
                'dependency_scanning': self._calculate_dependency_score(),
                'deployment_security': self._calculate_deployment_score(),
                'access_control': self._calculate_access_control_score()
            }
        else:  # VENDOR
            weights = risk_params.vendor_weights
            thresholds = risk_params.vendor_thresholds
            
            # Example scoring for vendor applications
            scores = {
                'vendor_assessment': self._calculate_vendor_score(),
                'contract_security': self._calculate_contract_score(),
                'integration_security': self._calculate_integration_score(),
                'data_handling': self._calculate_data_handling_score(),
                'support_sla': self._calculate_sla_score()
            }

        # Calculate weighted score
        total_score = sum(scores[key] * weights[key] for key in weights)
        max_possible = sum(100 * weight for weight in weights.values())

        # Convert to percentage
        final_score = (total_score / max_possible) * 100 if max_possible > 0 else 0
        
        # Store the score in score history
        score_history = ScoreHistory(
            application_id=self.id,
            score=final_score,
            created_at=datetime.utcnow()
        )
        db.session.add(score_history)
        
        return final_score

    def _calculate_code_review_score(self):
        """Calculate score based on code review practices"""
        # TODO: Implement actual calculation based on:
        # - Code review coverage
        # - Review process maturity
        # - Automated checks
        return 85  # Placeholder score

    def _calculate_security_testing_score(self):
        """Calculate score based on security testing"""
        # TODO: Implement actual calculation based on:
        # - SAST/DAST coverage
        # - Penetration testing frequency
        # - Security bug resolution
        return 75  # Placeholder score

    def _calculate_dependency_score(self):
        """Calculate score based on dependency management"""
        # TODO: Implement actual calculation based on:
        # - Dependency scanning
        # - Vulnerability management
        # - Update frequency
        return 90  # Placeholder score

    def _calculate_deployment_score(self):
        """Calculate score based on deployment security"""
        # TODO: Implement actual calculation based on:
        # - Infrastructure as code
        # - Deployment automation
        # - Environment security
        return 80  # Placeholder score

    def _calculate_access_control_score(self):
        """Calculate score based on access control"""
        # TODO: Implement actual calculation based on:
        # - Authentication mechanisms
        # - Authorization controls
        # - Audit logging
        return 85  # Placeholder score

    def _calculate_vendor_score(self):
        """Calculate score based on vendor assessment"""
        # TODO: Implement actual calculation based on:
        # - Vendor security questionnaire
        # - Security certifications
        # - Incident history
        return 80  # Placeholder score

    def _calculate_contract_score(self):
        """Calculate score based on contract security"""
        # TODO: Implement actual calculation based on:
        # - Security requirements
        # - SLA commitments
        # - Liability coverage
        return 85  # Placeholder score

    def _calculate_integration_score(self):
        """Calculate score based on integration security"""
        # TODO: Implement actual calculation based on:
        # - API security
        # - Data transmission
        # - Authentication methods
        return 75  # Placeholder score

    def _calculate_data_handling_score(self):
        """Calculate score based on data handling"""
        # TODO: Implement actual calculation based on:
        # - Data classification
        # - Privacy controls
        # - Data retention
        return 90  # Placeholder score

    def _calculate_sla_score(self):
        """Calculate score based on SLA compliance"""
        # TODO: Implement actual calculation based on:
        # - Response time
        # - Resolution time
        # - Support availability
        return 85  # Placeholder score

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'app_type': self.app_type,
            'vendor_name': self.vendor_name,
            'vendor_contact': self.vendor_contact,
            'support_url': self.support_url,
            'security_score': self.security_score,
            'last_scored': self.last_scored.isoformat() if self.last_scored else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'team_id': self.team_id,
            'catalog_id': self.catalog_id,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'team': self.team.to_dict() if self.team else None
        }
