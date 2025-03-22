"""
Security Score Card - Base Classes

Base classes providing common functionality across the application.

Authors:
    Clement Ellango
    Carolina Clement

Copyright (c) 2024. All rights reserved.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from flask import jsonify
from .constants import MESSAGES, SCORE_RANGES

class BaseAPIEndpoint:
    """Base class for API endpoints providing common functionality."""
    
    @staticmethod
    def handle_error(error: Exception, status_code: int = 500) -> tuple:
        """Standard error handling for API endpoints."""
        error_response = {
            'status': 'error',
            'message': str(error),
            'timestamp': datetime.utcnow().isoformat()
        }
        return jsonify(error_response), status_code

    @staticmethod
    def format_response(
        data: Any,
        status: str = 'success',
        message: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Standard response formatting."""
        response = {
            'status': status,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        if message:
            response['message'] = message
        if metadata:
            response['metadata'] = metadata
        return response

class BaseSecurityTool:
    """Base class for security tool integrations."""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    async def get_findings(self, application_id: str) -> List[Dict]:
        """Base method for getting security findings."""
        raise NotImplementedError("Subclasses must implement get_findings")

    async def get_score(self, application_id: str) -> float:
        """Base method for getting security score."""
        raise NotImplementedError("Subclasses must implement get_score")

class BaseDataService:
    """Base class for data services."""
    
    def __init__(self, session: Session):
        self.session = session

    def validate_score(self, score: float) -> float:
        """Validate and normalize a security score."""
        if score < 0:
            return 0
        if score > 100:
            return 100
        return round(score, 2)

    def get_risk_level(self, score: float) -> str:
        """Get risk level based on score."""
        for level, (min_score, max_score) in SCORE_RANGES.items():
            if min_score <= score <= max_score:
                return level
        return 'unknown'

    def format_timestamp(self, dt: datetime) -> str:
        """Format timestamp for consistent API responses."""
        return dt.isoformat() if dt else None
