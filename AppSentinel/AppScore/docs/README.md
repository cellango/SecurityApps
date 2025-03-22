# Application Security Score Card Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [API Reference](#api-reference)
5. [Frontend Components](#frontend-components)
6. [Database Schema](#database-schema)
7. [Security Considerations](#security-considerations)

## Overview

The Application Security Score Card is a web-based system for tracking and visualizing security metrics across different applications. It provides a centralized dashboard for security teams to monitor, record, and analyze security scores across various security categories.

### Key Features
- Multi-application security tracking
- Time-series visualization of security scores
- Categorized security assessments
- Detailed findings management
- Interactive dashboards
- RESTful API integration

## Architecture

### Technology Stack
- **Frontend**: React 18.2.0, Material-UI 5.14.9
- **Backend**: Flask 2.3.3, SQLAlchemy 2.0.21
- **Database**: PostgreSQL
- **Charts**: Chart.js 4.4.0
- **API Communication**: Axios 1.5.0

### System Components
```
security-score-card/
├── backend/
│   ├── app.py           # Flask application and API endpoints
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment configuration
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── App.js      # Main application component
│   │   └── index.js    # Application entry point
│   └── package.json    # Node.js dependencies
└── docs/              # Documentation
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. Create PostgreSQL Database:
```sql
CREATE DATABASE security_score_card;
```

2. Install Python Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure Environment:
Create `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/security_score_card
FLASK_ENV=development
FLASK_APP=app.py
```

4. Initialize Database:
```bash
flask run
```

### Frontend Setup

1. Install Dependencies:
```bash
cd frontend
npm install
```

2. Start Development Server:
```bash
npm start
```

## API Reference

### Applications

#### GET /api/applications
Returns a list of all applications.

Response:
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

#### POST /api/applications
Create a new application.

Request:
```json
{
  "name": "New Application",
  "description": "Application description"
}
```

### Security Scores

#### GET /api/applications/{id}/scores
Returns security scores for a specific application.

Response:
```json
[
  {
    "id": 1,
    "category": "Authentication",
    "score": 85.5,
    "findings": {
      "details": "Authentication findings..."
    },
    "created_at": "2024-12-26T12:00:00Z"
  }
]
```

#### POST /api/applications/{id}/scores
Add a new security score.

Request:
```json
{
  "category": "Authentication",
  "score": 85.5,
  "findings": {
    "details": "Authentication findings..."
  }
}
```

## Frontend Components

### ApplicationList
Main dashboard displaying all applications with summary information.

### ApplicationDetail
Detailed view of an application's security scores with interactive charts.

### AddApplication
Form component for adding new applications to the system.

### Navbar
Navigation component with links to main sections.

## Database Schema

### Application Table
```sql
CREATE TABLE application (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SecurityScore Table
```sql
CREATE TABLE security_score (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES application(id),
    category VARCHAR(50) NOT NULL,
    score FLOAT NOT NULL,
    findings JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Considerations

### Data Protection
- All database connections use parameterized queries to prevent SQL injection
- Frontend uses HTTPS for API communication
- Sensitive data is not logged

### Best Practices
- Input validation on both frontend and backend
- CORS configuration to restrict API access
- Error handling and logging
- Regular security score updates
- Detailed findings documentation

### Security Categories
1. **Authentication**
   - Identity verification
   - Password policies
   - Multi-factor authentication

2. **Authorization**
   - Access control
   - Role-based permissions
   - Resource protection

3. **Data Protection**
   - Encryption
   - Data handling
   - Privacy compliance

4. **Network Security**
   - Firewall configuration
   - Network segmentation
   - Traffic monitoring

5. **Code Security**
   - Code review findings
   - Dependency scanning
   - Security testing results
