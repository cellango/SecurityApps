# API Documentation

## Base URL
All API endpoints are relative to: `http://localhost:5000/api`

## Authentication
Currently, the API does not require authentication. For production deployment, implement appropriate authentication mechanisms.

## Endpoints

### Applications

#### List Applications
```http
GET /applications
```

Returns a list of all applications in the system.

**Response**
```json
[
  {
    "id": 1,
    "name": "Example App",
    "description": "Application description",
    "created_at": "2024-12-26T12:00:00Z"
  }
]
```

**Status Codes**
- 200: Success
- 500: Server Error

#### Create Application
```http
POST /applications
```

Create a new application.

**Request Body**
```json
{
  "name": "New Application",
  "description": "Application description"
}
```

**Response**
```json
{
  "id": 1,
  "name": "New Application",
  "description": "Application description",
  "created_at": "2024-12-26T12:00:00Z"
}
```

**Status Codes**
- 201: Created
- 400: Bad Request
- 500: Server Error

### Security Scores

#### Get Application Scores
```http
GET /applications/{id}/scores
```

Returns all security scores for a specific application.

**Parameters**
- `id`: Application ID (integer)

**Response**
```json
[
  {
    "id": 1,
    "category": "Authentication",
    "score": 85.5,
    "findings": {
      "strengths": [
        "MFA implemented",
        "Password policy enforced"
      ],
      "weaknesses": [
        "Session timeout too long"
      ]
    },
    "created_at": "2024-12-26T12:00:00Z"
  }
]
```

**Status Codes**
- 200: Success
- 404: Application Not Found
- 500: Server Error

#### Add Security Score
```http
POST /applications/{id}/scores
```

Add a new security score for an application.

**Parameters**
- `id`: Application ID (integer)

**Request Body**
```json
{
  "category": "Authentication",
  "score": 85.5,
  "findings": {
    "strengths": [
      "MFA implemented",
      "Password policy enforced"
    ],
    "weaknesses": [
      "Session timeout too long"
    ]
  }
}
```

**Response**
```json
{
  "id": 1,
  "category": "Authentication",
  "score": 85.5,
  "findings": {
    "strengths": [
      "MFA implemented",
      "Password policy enforced"
    ],
    "weaknesses": [
      "Session timeout too long"
    ]
  },
  "created_at": "2024-12-26T12:00:00Z"
}
```

**Status Codes**
- 201: Created
- 400: Bad Request
- 404: Application Not Found
- 500: Server Error

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider adding rate limiting to protect the API from abuse.

## Versioning

The API is currently at v1. Future versions will be accessed via URL versioning (e.g., `/api/v2/applications`).

## Data Types

### Application Object
| Field       | Type      | Description                    |
|-------------|-----------|--------------------------------|
| id          | integer   | Unique identifier              |
| name        | string    | Application name               |
| description | string    | Application description        |
| created_at  | timestamp | Creation timestamp (ISO 8601)  |

### Security Score Object
| Field         | Type      | Description                    |
|---------------|-----------|--------------------------------|
| id            | integer   | Unique identifier              |
| application_id| integer   | Reference to application       |
| category      | string    | Security category              |
| score         | float     | Numerical score (0-100)        |
| findings      | json      | Detailed findings              |
| created_at    | timestamp | Creation timestamp (ISO 8601)  |

## Security Categories
Available security categories:
- Authentication
- Authorization
- Data Protection
- Network Security
- Code Security
