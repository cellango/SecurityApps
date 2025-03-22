import aiohttp
from datetime import datetime
from typing import List, Dict
from . import SecurityToolIntegration, SecurityFinding

class VeracodeIntegration(SecurityToolIntegration):
    def __init__(self):
        api_key = os.getenv('VERACODE_API_KEY')
        api_secret = os.getenv('VERACODE_API_SECRET')
        base_url = 'https://api.veracode.com/appsec/v1'
        super().__init__(api_key, base_url)
        self.api_secret = api_secret

    async def get_findings(self, application_id: str) -> List[SecurityFinding]:
        """Get Veracode static analysis findings"""
        try:
            async with aiohttp.ClientSession() as session:
                # Get latest scan
                async with session.get(
                    f'{self.base_url}/applications/{application_id}/findings',
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    return [
                        SecurityFinding(
                            title=finding['title'],
                            severity=finding['severity'],
                            tool_name='Veracode',
                            finding_type='sast_finding',
                            description=finding.get('description', ''),
                            created_at=datetime.fromisoformat(finding['finding_status']['first_found_date']),
                            status=finding['finding_status']['status'],
                            remediation=finding.get('remediation_guidance'),
                            metadata={
                                'cwe': finding.get('cwe', {}).get('id'),
                                'cwe_name': finding.get('cwe', {}).get('name'),
                                'file_name': finding.get('finding_details', {}).get('file_name'),
                                'line_number': finding.get('finding_details', {}).get('line_number'),
                                'exploit_difficulty': finding.get('exploit_difficulty')
                            }
                        )
                        for finding in data.get('_embedded', {}).get('findings', [])
                    ]
        except Exception as e:
            print(f"Error fetching Veracode findings: {str(e)}")
            return []

    async def get_score(self, application_id: str) -> float:
        """Get security score from Veracode"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/applications/{application_id}/summary_report',
                    headers=self.headers
                ) as response:
                    data = await response.json()
                    
                    # Veracode policy score (0-100)
                    policy_score = data.get('policy_score', 100)
                    
                    # Additional factors
                    findings = await self.get_findings(application_id)
                    
                    # Deductions for open high/critical findings
                    critical_count = sum(1 for f in findings if f.severity == 'Critical' and f.status == 'OPEN')
                    high_count = sum(1 for f in findings if f.severity == 'High' and f.status == 'OPEN')
                    
                    # Adjust score based on critical/high findings
                    score = policy_score
                    score -= critical_count * 10  # -10 points per critical
                    score -= high_count * 5      # -5 points per high
                    
                    return max(0, score)
        except Exception as e:
            print(f"Error fetching Veracode score: {str(e)}")
            return 0.0

    async def get_compliance_status(self, application_id: str) -> Dict:
        """Get compliance status from Veracode"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.base_url}/applications/{application_id}/policy_compliance',
                    headers=self.headers
                ) as response:
                    compliance_data = await response.json()
                    
                    return {
                        'policy_compliance_status': compliance_data.get('policy_compliance_status'),
                        'policy_name': compliance_data.get('policy_name'),
                        'policy_version': compliance_data.get('policy_version'),
                        'last_scan_date': compliance_data.get('last_scan_date'),
                        'grace_period_expired': compliance_data.get('grace_period_expired'),
                        'scan_frequency_status': compliance_data.get('scan_frequency', {}).get('status')
                    }
        except Exception as e:
            print(f"Error fetching Veracode compliance: {str(e)}")
            return {}
