# Security Score Card - Scoring Methodology

Authors: Clement Ellango, Carolina Clement  
Copyright (c) 2024. All rights reserved.

## Overview

The Security Score Card system uses a weighted scoring methodology that adapts based on whether an application is internally developed or provided by a vendor. Each application type has its own set of criteria, weights, and thresholds that can be customized to match your organization's security requirements.

## Scoring Formula

The final security score is calculated using a hybrid approach that combines rules-based scoring and machine learning predictions:

```
Final Score = (Rules Score × 0.7) + (ML Score × 0.3)
```

### Rules-Based Scoring (70% Weight)

The rules-based score starts with a base score of 100 and applies deductions based on security findings:

1. **Rule Types and Impacts:**
   - Authentication Issues (e.g., Missing MFA): -20 points
   - Critical Vulnerabilities: -30 points per finding
   - High Vulnerabilities: -15 points per finding
   - Medium Vulnerabilities: -8 points per finding
   - Low Vulnerabilities: -3 points per finding
   - Compliance Violations: -10 points per violation
   - Missing Security Controls: -5 to -15 points depending on severity

2. **Application Type-Specific Rules:**
   - Internal Applications:
     ```
     Internal Score = Base Score - Σ(Security Deductions) × Internal Weights
     ```
   - Vendor Applications:
     ```
     Vendor Score = Base Score - Σ(Security Deductions) × Vendor Weights
     ```

3. **Rule Categories:**
   - Authentication & Access Control
   - Vulnerability Management
   - Code Security
   - Compliance
   - Operational Security

### Machine Learning Approach (30% Weight)

The ML-based scoring uses a supervised learning approach trained on historical security data:

1. **Feature Engineering:**
   ```python
   Features = [
       'critical_vulns',        # Number of critical vulnerabilities
       'high_vulns',           # Number of high vulnerabilities
       'medium_vulns',         # Number of medium vulnerabilities
       'low_vulns',            # Number of low vulnerabilities
       'outdated_deps_percentage', # Percentage of outdated dependencies
       'compliance_violations', # Number of compliance violations
       'security_hotspots',    # Number of security hotspots
       'code_coverage',        # Percentage of code coverage
       'duplicate_lines'       # Percentage of duplicate code
   ]
   ```

2. **Model Architecture:**
   - Uses a gradient boosting model (XGBoost/LightGBM)
   - Features are normalized using standard scaling
   - Model is retrained periodically with new data
   - Predictions are bounded between 0 and 100

3. **Training Process:**
   - Historical security scores and findings are used as training data
   - Model is validated using k-fold cross-validation
   - Feature importance is tracked to understand key factors
   - Model versions are stored and can be rolled back if needed

4. **Prediction Process:**
   ```
   1. Collect current security metrics
   2. Normalize features using stored scaler
   3. Generate prediction using latest model
   4. Apply bounds (0-100) to final score
   ```

## Application Types

### 1. Internal Applications
Applications that are developed and maintained internally by your organization.

#### Scoring Criteria:
1. **Code Review (30%)**
   - Code review coverage
   - Review process maturity
   - Automated code analysis
   - Pull request approval process

2. **Security Testing (20%)**
   - SAST/DAST coverage
   - Penetration testing frequency
   - Security bug resolution time
   - Test coverage metrics

3. **Dependency Scanning (20%)**
   - Dependency scanning frequency
   - Vulnerability management
   - Update frequency
   - License compliance

4. **Deployment Security (15%)**
   - Infrastructure as code
   - Deployment automation
   - Environment security
   - Secret management

5. **Access Control (15%)**
   - Authentication mechanisms
   - Authorization controls
   - Audit logging
   - Role-based access control

### 2. Vendor Applications
Applications that are provided by third-party vendors.

#### Scoring Criteria:
1. **Vendor Assessment (30%)**
   - Security questionnaire results
   - Security certifications
   - Incident history
   - Compliance status

2. **Contract Security (20%)**
   - Security SLAs
   - Incident response requirements
   - Data handling agreements
   - Compliance commitments

3. **Integration Security (20%)**
   - API security controls
   - Authentication methods
   - Data encryption
   - Access management

4. **Data Handling (15%)**
   - Data classification
   - Data storage location
   - Backup procedures
   - Data retention policies

5. **Support SLA (15%)**
   - Response time commitments
   - Update frequency
   - Patch management
   - Technical support quality

## Risk Thresholds

Applications are categorized into risk levels based on their security scores:

1. **High Risk**: Score < 60
   - Immediate attention required
   - Weekly security reviews
   - Restricted deployment capabilities

2. **Medium Risk**: Score 60-80
   - Regular monitoring
   - Monthly security reviews
   - Normal deployment with additional approvals

3. **Low Risk**: Score 80-90
   - Standard monitoring
   - Quarterly security reviews
   - Normal deployment procedures

4. **Minimal Risk**: Score > 90
   - Routine monitoring
   - Semi-annual security reviews
   - Streamlined deployment procedures

## API Documentation

### 1. Get Current Risk Parameters

```http
GET /api/risk-parameters
Authorization: Bearer <your-token>
```

Response:
```json
{
  "id": 1,
  "internal_weights": {
    "code_review": 0.3,
    "security_testing": 0.2,
    "dependency_scanning": 0.2,
    "deployment_security": 0.15,
    "access_control": 0.15
  },
  "internal_thresholds": {
    "high_risk": 60,
    "medium_risk": 80,
    "low_risk": 90
  },
  "vendor_weights": {
    "vendor_assessment": 0.3,
    "contract_security": 0.2,
    "integration_security": 0.2,
    "data_handling": 0.15,
    "support_sla": 0.15
  },
  "vendor_thresholds": {
    "high_risk": 60,
    "medium_risk": 80,
    "low_risk": 90
  }
}
```

### 2. Update Risk Parameters

```http
PUT /api/risk-parameters
Authorization: Bearer <your-token>
Content-Type: application/json

{
  "internal_weights": {
    "code_review": 0.25,
    "security_testing": 0.25,
    "dependency_scanning": 0.20,
    "deployment_security": 0.15,
    "access_control": 0.15
  },
  "internal_thresholds": {
    "high_risk": 65,
    "medium_risk": 85,
    "low_risk": 95
  }
}
```

Note: You can update individual components (weights or thresholds) for either internal or vendor applications. All fields are optional in the update request.

### 3. Calculate Risk Score for an Application

```http
POST /api/applications/{app_id}/calculate-risk
Authorization: Bearer <your-token>
```

Response:
```json
{
  "application_id": 123,
  "security_score": 85.5,
  "last_scored": "2024-12-28T13:23:02Z"
}
```

## Security Tools Integration

The scoring system integrates with various security tools to gather data:

1. **SonarQube**
   - Code quality metrics
   - Security hotspots
   - Code coverage

2. **Snyk**
   - Dependency vulnerabilities
   - License compliance
   - Container security

3. **Black Duck**
   - Open source security
   - License compliance
   - Component analysis

4. **Veracode**
   - Static analysis
   - Dynamic analysis
   - Software composition analysis

## Best Practices

1. **Regular Updates**
   - Scores should be updated at least weekly
   - Critical findings should trigger immediate rescoring
   - Historical trends should be monitored

2. **Customization**
   - Weights can be adjusted to match organizational priorities
   - Thresholds can be modified based on risk tolerance
   - New criteria can be added as security practices evolve

3. **API Security**
   - All API endpoints require authentication
   - Parameter updates should be restricted to authorized users
   - API calls are rate-limited to prevent abuse

## Implementation Notes

1. **Score Calculation**
   - Scores are calculated as weighted averages
   - Individual criteria scores range from 0-100
   - Final score is normalized to 0-100 scale

2. **Data Storage**
   - Score history is maintained for trend analysis
   - Parameters are stored in the risk_parameters table
   - Changes to parameters are logged for audit purposes
