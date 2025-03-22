import aiohttp
from datetime import datetime
from typing import List, Dict
from . import SecurityToolIntegration, SecurityFinding

class SonarQubeIntegration(SecurityToolIntegration):
    def __init__(self):
        api_key = os.getenv('SONARQUBE_API_KEY')
        base_url = os.getenv('SONARQUBE_URL', 'http://localhost:9000')
        super().__init__(api_key, base_url)

    async def get_findings(self, application_id: str) -> List[SecurityFinding]:
        """Get SonarQube security issues for an application"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/api/issues/search',
                    headers=self.headers,
                    params={
                        'componentKeys': application_id,
                        'types': 'VULNERABILITY,SECURITY_HOTSPOT',
                        'resolved': 'false'
                    }
                ) as response:
                    data = await response.json()
                    return [
                        SecurityFinding(
                            title=issue['message'],
                            severity=issue['severity'],
                            tool_name='SonarQube',
                            finding_type='security_issue',
                            description=issue.get('description', ''),
                            created_at=datetime.fromisoformat(issue['creationDate']),
                            status=issue['status'],
                            metadata={
                                'rule': issue['rule'],
                                'file': issue.get('component'),
                                'line': issue.get('line'),
                                'effort': issue.get('effort')
                            }
                        )
                        for issue in data.get('issues', [])
                    ]
        except Exception as e:
            print(f"Error fetching SonarQube findings: {str(e)}")
            return []

    async def get_score(self, application_id: str) -> float:
        """Get security rating from SonarQube"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/api/measures/component',
                    headers=self.headers,
                    params={
                        'component': application_id,
                        'metricKeys': 'security_rating,security_review_rating,security_hotspots_reviewed'
                    }
                ) as response:
                    data = await response.json()
                    measures = {
                        measure['metric']: float(measure['value'])
                        for measure in data.get('component', {}).get('measures', [])
                    }

                    # Convert SonarQube's 1-5 rating to 0-100 score
                    security_score = 100 - (measures.get('security_rating', 1) - 1) * 20
                    review_score = 100 - (measures.get('security_review_rating', 1) - 1) * 20
                    hotspots_score = measures.get('security_hotspots_reviewed', 0)

                    # Weighted average
                    return (security_score * 0.4 + review_score * 0.3 + hotspots_score * 0.3)
        except Exception as e:
            print(f"Error fetching SonarQube score: {str(e)}")
            return 0.0

    async def get_compliance_status(self, application_id: str) -> Dict:
        """Get compliance status from SonarQube quality gates"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/api/qualitygates/project_status',
                    headers=self.headers,
                    params={'projectKey': application_id}
                ) as response:
                    data = await response.json()
                    return {
                        'status': data.get('projectStatus', {}).get('status'),
                        'conditions': data.get('projectStatus', {}).get('conditions', [])
                    }
        except Exception as e:
            print(f"Error fetching SonarQube compliance: {str(e)}")
            return {}
