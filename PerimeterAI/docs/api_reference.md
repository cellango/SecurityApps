# PerimeterAI API Reference

## Authentication

All API endpoints require authentication using JWT tokens obtained from Keycloak.

### Getting an Access Token

```http
POST /realms/{realm}/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&
client_id={client_id}&
client_secret={client_secret}&
username={username}&
password={password}
```

## Keyboard Dynamics Platform APIs

### Analytics Service API

#### Submit Keystroke Data
```http
POST /api/v1/collect
Authorization: Bearer {token}
Content-Type: application/json

{
  "userId": "string",
  "sessionId": "string",
  "keystrokes": [
    {
      "key": "string",
      "timestamp": "number",
      "eventType": "keydown|keyup",
      "pressure": "number"
    }
  ]
}
```

#### Analyze Typing Patterns
```http
POST /api/v1/analyze
Authorization: Bearer {token}
Content-Type: application/json

{
  "userId": "string",
  "sessionId": "string",
  "timeframe": "string"
}
```

#### Get Risk Score
```http
GET /api/v1/risk-score/{userId}
Authorization: Bearer {token}
```

#### Train Model
```http
POST /api/v1/models/train
Authorization: Bearer {token}
Content-Type: application/json

{
  "userId": "string",
  "modelType": "string",
  "parameters": {
    "key": "value"
  }
}
```

### Collector Service API

#### Submit Raw Keystroke Data
```http
POST /api/v1/keystrokes
Authorization: Bearer {token}
Content-Type: application/json

{
  "userId": "string",
  "deviceId": "string",
  "keystrokes": [
    {
      "key": "string",
      "timestamp": "number",
      "eventType": "string"
    }
  ]
}
```

#### Get Service Status
```http
GET /api/v1/status
Authorization: Bearer {token}
```

### Authentication Service API

#### Verify User
```http
POST /api/v1/auth/verify
Authorization: Bearer {token}
Content-Type: application/json

{
  "userId": "string",
  "sessionId": "string",
  "typingData": {
    "pattern": "array",
    "confidence": "number"
  }
}
```

#### Get Authentication Status
```http
GET /api/v1/auth/status/{sessionId}
Authorization: Bearer {token}
```

#### Update Authentication Policy
```http
PUT /api/v1/auth/policy
Authorization: Bearer {token}
Content-Type: application/json

{
  "riskThreshold": "number",
  "requiredConfidence": "number",
  "maxAttempts": "number"
}
```

## Signature Service API

### Document Operations

#### Sign Document
```http
POST /api/v1/signature/sign
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "document": "file",
  "certificateId": "string",
  "signatureType": "string",
  "metadata": {
    "key": "value"
  }
}
```

#### Verify Signature
```http
POST /api/v1/signature/verify
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "document": "file",
  "signature": "string"
}
```

### Certificate Management

#### List Certificates
```http
GET /api/v1/certificates
Authorization: Bearer {token}
```

#### Get Certificate Details
```http
GET /api/v1/certificates/{id}
Authorization: Bearer {token}
```

#### Create Certificate
```http
POST /api/v1/certificates
Authorization: Bearer {token}
Content-Type: application/json

{
  "subject": "string",
  "validityPeriod": "number",
  "keyType": "string",
  "keySize": "number"
}
```

### Audit Operations

#### Get Signature History
```http
GET /api/v1/signature/audit
Authorization: Bearer {token}
Query Parameters:
  - startDate: string
  - endDate: string
  - userId: string
```

#### Get Document Trail
```http
GET /api/v1/signature/audit/document/{documentId}
Authorization: Bearer {token}
```

## Policy Studio API

### Policy Management

#### List Policies
```http
GET /api/v1/policies
Authorization: Bearer {token}
Query Parameters:
  - type: string
  - status: string
  - version: string
```

#### Get Policy Details
```http
GET /api/v1/policies/{id}
Authorization: Bearer {token}
```

#### Create Policy
```http
POST /api/v1/policies
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "type": "string",
  "rules": [
    {
      "conditions": [
        {
          "attribute": "string",
          "operator": "string",
          "value": "any"
        }
      ],
      "actions": [
        {
          "type": "string",
          "parameters": {
            "key": "value"
          }
        }
      ]
    }
  ],
  "metadata": {
    "key": "value"
  }
}
```

#### Update Policy
```http
PUT /api/v1/policies/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "rules": [...],
  "metadata": {...}
}
```

#### Delete Policy
```http
DELETE /api/v1/policies/{id}
Authorization: Bearer {token}
```

### Policy Versioning

#### List Policy Versions
```http
GET /api/v1/policies/{id}/versions
Authorization: Bearer {token}
```

#### Get Specific Version
```http
GET /api/v1/policies/{id}/versions/{version}
Authorization: Bearer {token}
```

#### Create Version
```http
POST /api/v1/policies/{id}/versions
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "string",
  "rules": [...],
  "metadata": {...}
}
```

### Policy Deployment

#### Deploy Policy
```http
POST /api/v1/policies/{id}/deploy
Authorization: Bearer {token}
Content-Type: application/json

{
  "version": "string",
  "environment": "string",
  "parameters": {
    "key": "value"
  }
}
```

#### Get Deployment Status
```http
GET /api/v1/policies/{id}/deployments/{deploymentId}
Authorization: Bearer {token}
```

#### List Deployments
```http
GET /api/v1/policies/{id}/deployments
Authorization: Bearer {token}
```

### Policy Testing

#### Test Policy
```http
POST /api/v1/policies/{id}/test
Authorization: Bearer {token}
Content-Type: application/json

{
  "context": {
    "user": {...},
    "resource": {...},
    "environment": {...}
  }
}
```

#### Simulate Policy
```http
POST /api/v1/policies/{id}/simulate
Authorization: Bearer {token}
Content-Type: application/json

{
  "scenarios": [
    {
      "name": "string",
      "context": {...}
    }
  ]
}
```

## Tenant Management API

### List Tenants
```http
GET /admin/realms/{realm}/tenants
Authorization: Bearer {token}
```

### Create Tenant
```http
POST /admin/realms/{realm}/tenants
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "settings": {
    "key": "value"
  }
}
```

### Get Tenant Details
```http
GET /admin/realms/{realm}/tenants/{id}
Authorization: Bearer {token}
```

### Update Tenant
```http
PUT /admin/realms/{realm}/tenants/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "settings": {
    "key": "value"
  }
}
```

### Delete Tenant
```http
DELETE /admin/realms/{realm}/tenants/{id}
Authorization: Bearer {token}
```

## Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {
    // Response data
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## Rate Limits
- Authentication endpoints: 10 requests per minute
- Data collection endpoints: 100 requests per minute
- Analysis endpoints: 50 requests per minute
- Signature operations: 30 requests per minute
- Certificate operations: 20 requests per minute
- Policy Management endpoints: 40 requests per minute
- Policy Testing endpoints: 20 requests per minute
- Policy Deployment endpoints: 10 requests per minute

## Error Codes
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Resource not found
- `422`: Validation error
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable

## Best Practices
1. Always validate input data
2. Handle rate limits appropriately
3. Implement proper error handling
4. Use appropriate content types
5. Keep tokens secure
6. Log API usage for monitoring
7. Implement retry mechanisms with exponential backoff
8. Use webhook endpoints for long-running operations
9. Implement proper certificate validation
10. Follow security best practices for signature operations

## SDK Support
- Python SDK: [GitHub Repository]
- JavaScript SDK: [GitHub Repository]
- Java SDK: [GitHub Repository]
- Signature SDK: [GitHub Repository]
