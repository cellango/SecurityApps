"""
Security Score Card - Constants

Shared constants used throughout the application.

Authors:
    Clement Ellango
    Carolina Clement

Copyright (c) 2024. All rights reserved.
"""

from typing import Dict, Tuple

# Score ranges and their corresponding risk levels
SCORE_RANGES: Dict[str, Tuple[int, int]] = {
    'critical': (0, 30),
    'high': (31, 60),
    'medium': (61, 80),
    'low': (81, 100)
}

# Security finding severity levels
SEVERITY_LEVELS = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']

# Default weights for scoring components
SCORING_WEIGHTS = {
    'rules_based': 0.7,
    'ml_based': 0.3
}

# Security tool names
SECURITY_TOOLS = {
    'sonarqube': 'SonarQube',
    'snyk': 'Snyk',
    'blackduck': 'Black Duck',
    'veracode': 'Veracode'
}

# Application types
APPLICATION_TYPES = {
    'internal': 'Internal',
    'vendor': 'Vendor',
    'open_source': 'Open Source'
}

# Default pagination values
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Cache settings
CACHE_TTL = {
    'short': 300,  # 5 minutes
    'medium': 1800,  # 30 minutes
    'long': 86400  # 24 hours
}

# API response messages
MESSAGES = {
    'success': 'Operation completed successfully',
    'not_found': 'Resource not found',
    'validation_error': 'Validation error occurred',
    'unauthorized': 'Unauthorized access',
    'server_error': 'Internal server error occurred'
}

# Security score impact weights
SECURITY_IMPACT_WEIGHTS = {
    'authentication': {
        'mfa_missing': -20,
        'weak_password_policy': -15,
        'insecure_session': -10
    },
    'vulnerabilities': {
        'critical': -30,
        'high': -15,
        'medium': -8,
        'low': -3
    },
    'compliance': {
        'major_violation': -20,
        'minor_violation': -10
    }
}
