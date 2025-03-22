from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import os

class SecurityFinding:
    def __init__(self, 
                 title: str,
                 severity: str,
                 tool_name: str,
                 finding_type: str,
                 description: str,
                 created_at: datetime,
                 status: str = 'OPEN',
                 remediation: Optional[str] = None,
                 metadata: Optional[Dict] = None):
        self.title = title
        self.severity = severity
        self.tool_name = tool_name
        self.finding_type = finding_type
        self.description = description
        self.created_at = created_at
        self.status = status
        self.remediation = remediation
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'severity': self.severity,
            'tool_name': self.tool_name,
            'finding_type': self.finding_type,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'remediation': self.remediation,
            'metadata': self.metadata
        }

class SecurityToolIntegration(ABC):
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    @abstractmethod
    async def get_findings(self, application_id: str) -> List[SecurityFinding]:
        """Get security findings for an application"""
        pass

    @abstractmethod
    async def get_score(self, application_id: str) -> float:
        """Get security score for an application"""
        pass

    @abstractmethod
    async def get_compliance_status(self, application_id: str) -> Dict:
        """Get compliance status for an application"""
        pass
