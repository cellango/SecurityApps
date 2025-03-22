import aiohttp
from datetime import datetime
from typing import List, Dict
from . import SecurityToolIntegration, SecurityFinding

class BlackDuckIntegration(SecurityToolIntegration):
    def __init__(self):
        api_key = os.getenv('BLACKDUCK_API_KEY')
        base_url = os.getenv('BLACKDUCK_URL')
        super().__init__(api_key, base_url)

    async def get_findings(self, application_id: str) -> List[SecurityFinding]:
        """Get Black Duck security vulnerabilities"""
        try:
            async with aiohttp.ClientSession() as session:
                # First get project by application ID
                async with session.get(
                    f'{self.base_url}/api/projects/{application_id}',
                    headers=self.headers
                ) as response:
                    project = await response.json()

                # Then get vulnerabilities
                async with session.get(
                    f'{self.base_url}/api/projects/{project["id"]}/vulnerable-components',
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    return [
                        SecurityFinding(
                            title=vuln['vulnerabilityWithRemediation']['vulnerabilityName'],
                            severity=vuln['vulnerabilityWithRemediation']['severity'],
                            tool_name='Black Duck',
                            finding_type='vulnerability',
                            description=vuln['vulnerabilityWithRemediation']['description'],
                            created_at=datetime.fromisoformat(vuln['vulnerabilityWithRemediation']['publishDate']),
                            remediation=vuln['vulnerabilityWithRemediation'].get('solution'),
                            metadata={
                                'component': vuln.get('componentName'),
                                'version': vuln.get('componentVersionName'),
                                'cve': vuln['vulnerabilityWithRemediation'].get('cveId'),
                                'cwes': vuln['vulnerabilityWithRemediation'].get('cwes', [])
                            }
                        )
                        for vuln in data.get('items', [])
                    ]
        except Exception as e:
            print(f"Error fetching Black Duck findings: {str(e)}")
            return []

    async def get_score(self, application_id: str) -> float:
        """Calculate security score based on Black Duck findings"""
        findings = await self.get_findings(application_id)
        if not findings:
            return 100.0

        # Score deductions by severity
        deductions = {
            'CRITICAL': 25,
            'HIGH': 15,
            'MEDIUM': 7,
            'LOW': 3
        }

        # Additional deductions for findings with exploits
        exploit_deduction = 10

        score = 100
        for finding in findings:
            score -= deductions.get(finding.severity, 0)
            if finding.metadata.get('hasExploit'):
                score -= exploit_deduction

        return max(0, score)

    async def get_compliance_status(self, application_id: str) -> Dict:
        """Get compliance status from Black Duck"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/api/projects/{application_id}/policy-status',
                    headers=self.headers
                ) as response:
                    policy_status = await response.json()
                    
                    # Get license compliance
                    async with session.get(
                        f'{self.base_url}/api/projects/{application_id}/license-compliance',
                        headers=self.headers
                    ) as license_response:
                        license_status = await license_response.json()
                        
                        return {
                            'policy_status': policy_status.get('overallStatus'),
                            'policy_violations': policy_status.get('componentVersionStatusCounts', {}),
                            'license_compliance': license_status.get('status'),
                            'license_violations': license_status.get('violationCounts', {})
                        }
        except Exception as e:
            print(f"Error fetching Black Duck compliance: {str(e)}")
            return {}
