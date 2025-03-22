import aiohttp
from datetime import datetime
from typing import List, Dict
from . import SecurityToolIntegration, SecurityFinding

class SnykIntegration(SecurityToolIntegration):
    def __init__(self):
        api_key = os.getenv('SNYK_API_KEY')
        base_url = 'https://snyk.io/api/v1'
        super().__init__(api_key, base_url)

    async def get_findings(self, application_id: str) -> List[SecurityFinding]:
        """Get Snyk vulnerabilities for an application"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.base_url}/test',
                    headers=self.headers,
                    json={'applicationId': application_id}
                ) as response:
                    data = await response.json()
                    return [
                        SecurityFinding(
                            title=vuln['title'],
                            severity=vuln['severity'],
                            tool_name='Snyk',
                            finding_type='vulnerability',
                            description=vuln['description'],
                            created_at=datetime.fromisoformat(vuln['createdAt']),
                            remediation=vuln.get('remediation'),
                            metadata={
                                'package_name': vuln.get('package'),
                                'version': vuln.get('version'),
                                'cve': vuln.get('identifiers', {}).get('CVE', [])
                            }
                        )
                        for vuln in data.get('vulnerabilities', [])
                    ]
        except Exception as e:
            print(f"Error fetching Snyk findings: {str(e)}")
            return []

    async def get_score(self, application_id: str) -> float:
        """Calculate security score based on Snyk findings"""
        findings = await self.get_findings(application_id)
        if not findings:
            return 100.0

        # Score deductions by severity
        deductions = {
            'critical': 20,
            'high': 10,
            'medium': 5,
            'low': 2
        }

        score = 100
        for finding in findings:
            score -= deductions.get(finding.severity.lower(), 0)

        return max(0, score)

    async def get_compliance_status(self, application_id: str) -> Dict:
        """Get compliance status from Snyk"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/test/{application_id}/compliance',
                    headers=self.headers
                ) as response:
                    return await response.json()
        except Exception as e:
            print(f"Error fetching Snyk compliance: {str(e)}")
            return {}
