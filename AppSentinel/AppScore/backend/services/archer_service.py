import os
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ArcherService:
    def __init__(self):
        self.base_url = os.getenv('ARCHER_API_URL')
        self.api_key = os.getenv('ARCHER_API_KEY')
        self.instance_name = os.getenv('ARCHER_INSTANCE')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Archer-Instance': self.instance_name
        }

    async def get_application_details(self, app_name):
        """Get application details from Archer."""
        try:
            response = await requests.get(
                f"{self.base_url}/api/v2/applications",
                headers=self.headers,
                params={'name': app_name}
            )
            response.raise_for_status()
            data = response.json()
            
            if not data['records']:
                return None

            record = data['records'][0]
            return {
                'archer_id': record.get('id'),
                'business_unit': record.get('business_unit'),
                'data_classification': record.get('data_classification'),
                'risk_rating': record.get('risk_rating'),
                'compliance_status': record.get('compliance_status'),
                'last_assessment_date': record.get('last_assessment_date'),
                'next_assessment_date': record.get('next_assessment_date'),
                'controls': record.get('controls', []),
                'findings': record.get('findings', []),
                'exceptions': record.get('exceptions', [])
            }
        except Exception as e:
            logger.error(f"Error fetching Archer data: {str(e)}")
            return None

    async def get_compliance_requirements(self, app_name):
        """Get compliance requirements from Archer."""
        try:
            response = await requests.get(
                f"{self.base_url}/api/v2/compliance",
                headers=self.headers,
                params={'application': app_name}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'frameworks': data.get('frameworks', []),
                'requirements': data.get('requirements', []),
                'status': data.get('status', {}),
                'last_updated': data.get('last_updated')
            }
        except Exception as e:
            logger.error(f"Error fetching compliance data: {str(e)}")
            return None

    async def get_risk_assessment(self, app_name):
        """Get risk assessment details from Archer."""
        try:
            response = await requests.get(
                f"{self.base_url}/api/v2/risk-assessment",
                headers=self.headers,
                params={'application': app_name}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'inherent_risk': data.get('inherent_risk', {}),
                'residual_risk': data.get('residual_risk', {}),
                'risk_factors': data.get('risk_factors', []),
                'mitigating_controls': data.get('mitigating_controls', []),
                'assessment_date': data.get('assessment_date')
            }
        except Exception as e:
            logger.error(f"Error fetching risk assessment: {str(e)}")
            return None
