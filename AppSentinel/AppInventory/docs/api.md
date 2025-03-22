# API Documentation

## Overview
AppSentinel provides a RESTful API for managing security controls and generating reports. All endpoints return JSON responses and accept JSON payloads where applicable.

## Base URL
```
http://localhost:5000/api
```

## Authentication
Authentication is required for all API endpoints. Use the Authorization header with a Bearer token:
```
Authorization: Bearer <your-token>
```

## Endpoints

### Dashboard Controls

#### Get Dashboard Data
```http
GET /dashboard/controls
```
Returns aggregated data for the security controls dashboard.

**Response**
```json
{
  "total_controls": 100,
  "by_status": {
    "implemented": 50,
    "partially_implemented": 25,
    "planned": 15,
    "not_implemented": 10
  },
  "by_family": {
    "access_control": 30,
    "configuration_management": 20,
    "incident_response": 15,
    "risk_assessment": 15,
    "system_communications": 10,
    "system_information": 10
  }
}
```

#### Export Controls
```http
GET /dashboard/controls/export
```
Export controls data in CSV or Excel format.

**Query Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| format | string | Either 'csv' or 'excel' |
| department | string | Filter by department |
| team | string | Filter by team |
| family | string | Filter by control family |
| status | string | Filter by implementation status |
| implementation_date_start | date | Filter by implementation date range start |
| implementation_date_end | date | Filter by implementation date range end |

**Response**
File download in requested format.

### Filter Presets

#### Get Filter Suggestions
```http
GET /dashboard/filters/suggestions
```
Get suggestions for filter values based on existing data.

**Response**
```json
{
  "departments": ["Engineering", "IT Security"],
  "teams": ["Frontend", "Backend"],
  "control_families": ["ACCESS_CONTROL", "CONFIGURATION_MANAGEMENT"],
  "statuses": ["IMPLEMENTED", "PARTIALLY_IMPLEMENTED"],
  "implementation_date_range": {
    "min": "2024-01-01",
    "max": "2024-12-31"
  }
}
```

#### List Filter Presets
```http
GET /dashboard/filters/presets
```
Get all saved filter presets.

**Response**
```json
[
  {
    "id": 1,
    "name": "Engineering Controls",
    "department": "Engineering",
    "team": "Frontend",
    "control_family": "ACCESS_CONTROL",
    "status": "IMPLEMENTED",
    "implementation_date_start": "2024-01-01",
    "implementation_date_end": "2024-12-31",
    "created_at": "2024-12-28T14:00:00Z",
    "last_used": "2024-12-28T14:30:00Z"
  }
]
```

#### Create Filter Preset
```http
POST /dashboard/filters/presets
```

**Request Body**
```json
{
  "name": "Engineering Controls",
  "department": "Engineering",
  "team": "Frontend",
  "control_family": "ACCESS_CONTROL",
  "status": "IMPLEMENTED",
  "implementation_date_start": "2024-01-01",
  "implementation_date_end": "2024-12-31"
}
```

**Response**
```json
{
  "id": 1,
  "name": "Engineering Controls",
  "created_at": "2024-12-28T14:00:00Z"
}
```

#### Delete Filter Preset
```http
DELETE /dashboard/filters/presets/{preset_id}
```
Delete a saved filter preset.

**Response**
204 No Content

#### Use Filter Preset
```http
POST /dashboard/filters/presets/{preset_id}/use
```
Mark a filter preset as used.

**Response**
```json
{
  "id": 1,
  "last_used": "2024-12-28T14:30:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting
API requests are limited to 100 requests per minute per IP address.

## Versioning
The current API version is v1. The version is included in the base URL:
```
/api/v1/...
```
