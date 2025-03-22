# Database Design Documentation

## Overview
AppSentinel uses a PostgreSQL database to store application security control information. The database schema is designed to support efficient tracking and reporting of security controls across different departments and teams.

## Entity Relationship Diagram
```
+-------------------+     +----------------------+     +------------------+
|    Application    |     |   SecurityControl    |     | ExportFilterPreset|
+-------------------+     +----------------------+     +------------------+
| id                |     | id                   |     | id               |
| name              |     | name                 |     | name             |
| department_name   |     | description          |     | department       |
| team_name         |     | control_family       |     | team            |
| description       |     | implementation_status|     | control_family   |
| created_at        |     | implementation_date  |     | status          |
| updated_at        |<--->| application_id       |     | impl_date_start |
+-------------------+     | created_at           |     | impl_date_end   |
                         | updated_at            |     | created_at      |
                         +----------------------+     | last_used       |
                                                    +------------------+
```

## Tables

### Application
Stores information about applications in the organization.

| Column         | Type         | Description                    |
|---------------|--------------|--------------------------------|
| id            | Integer      | Primary key                    |
| name          | String(100)  | Application name               |
| department_name| String(100)  | Department responsible         |
| team_name     | String(100)  | Team responsible               |
| description   | Text         | Application description        |
| created_at    | DateTime     | Record creation timestamp      |
| updated_at    | DateTime     | Last update timestamp          |

### SecurityControl
Tracks security controls implemented in applications.

| Column              | Type         | Description                    |
|--------------------|--------------|--------------------------------|
| id                 | Integer      | Primary key                    |
| name               | String(100)  | Control name                   |
| description        | Text         | Control description            |
| control_family     | Enum         | Category of control            |
| implementation_status| Enum       | Current status                 |
| implementation_date| Date         | When implemented               |
| application_id     | Integer      | Foreign key to Application     |
| created_at         | DateTime     | Record creation timestamp      |
| updated_at         | DateTime     | Last update timestamp          |

### ExportFilterPreset
Stores saved filter configurations for report exports.

| Column                | Type         | Description                    |
|----------------------|--------------|--------------------------------|
| id                   | Integer      | Primary key                    |
| name                 | String(100)  | Preset name                    |
| department           | String(100)  | Department filter              |
| team                 | String(100)  | Team filter                    |
| control_family       | Enum         | Control family filter          |
| status               | Enum         | Implementation status filter   |
| implementation_date_start| Date     | Start date filter              |
| implementation_date_end  | Date     | End date filter                |
| created_at           | DateTime     | Record creation timestamp      |
| last_used            | DateTime     | Last usage timestamp           |

## Enums

### ControlFamily
```python
class ControlFamily(enum.Enum):
    ACCESS_CONTROL = "ACCESS_CONTROL"
    CONFIGURATION_MANAGEMENT = "CONFIGURATION_MANAGEMENT"
    INCIDENT_RESPONSE = "INCIDENT_RESPONSE"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    SYSTEM_COMMUNICATIONS = "SYSTEM_COMMUNICATIONS"
    SYSTEM_INFORMATION = "SYSTEM_INFORMATION"
```

### ControlStatus
```python
class ControlStatus(enum.Enum):
    IMPLEMENTED = "IMPLEMENTED"
    PARTIALLY_IMPLEMENTED = "PARTIALLY_IMPLEMENTED"
    PLANNED = "PLANNED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
```

## Relationships
- One-to-Many relationship between Application and SecurityControl
- No direct relationships for ExportFilterPreset (used for storing UI preferences)

## Indexes
- Primary key indexes on all id columns
- Foreign key index on SecurityControl.application_id
- Index on Application.department_name and Application.team_name for filtering
- Index on SecurityControl.implementation_date for date range queries

## Data Integrity
- Foreign key constraints ensure referential integrity
- NOT NULL constraints on required fields
- Enum constraints ensure valid values for control_family and status
- Timestamp fields automatically updated

## Migrations
Database migrations are managed using Alembic through Flask-Migrate:
- Migrations are stored in `/migrations/versions/`
- Run migrations: `flask db upgrade`
- Create new migration: `flask db migrate -m "description"`
