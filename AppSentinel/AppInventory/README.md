# AppInventory

A centralized application inventory management system that helps security teams track and manage all applications within their organization.

## Authors

- **Clement Ellango** - *Lead Developer* - Security Architecture and Backend Development
- **Carolina Clement** - *Lead Developer* - Frontend Development and Security Engineering

## Overview
AppSentinel is a comprehensive application security control management system that helps organizations track, monitor, and report on security controls across their application portfolio. The system provides a dashboard for visualizing control implementation status, exporting filtered reports, and managing security compliance.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Documentation](#documentation)
5. [Contributing](#contributing)
6. [License](#license)

## Features
- Centralized application inventory management
- Real-time application health monitoring
- Automated security control tracking
- Role-based access control
- Task queue system for application lifecycle management
- Periodic health checks and metadata updates
- Real-time monitoring dashboard
- Interactive dashboard for security control visualization
- Filtered export functionality with preset management
- Department and team-based organization
- Control family categorization
- Implementation status tracking
- Detailed reporting capabilities

## Architecture
The system consists of several components:

1. **Frontend**: React-based web interface
2. **Backend API**: Flask-based REST API
3. **Database**: PostgreSQL for data persistence
4. **Task Queue**: Celery with Redis for async operations
5. **Monitoring**: Flower dashboard for task monitoring

## Navigation and Features

### Landing Page (Home)
The landing page serves as the main entry point for AppInventory, providing:
- Overview of your application inventory
- Quick access to common tasks
- System status and notifications
- Recent updates and announcements

Access via:
- Click AppSentinel logo
- Click Home tab in navigation bar
- Select Home from user menu
- Navigate to `/`

### Dashboard
The dashboard provides comprehensive insights into your application security posture:

#### Key Metrics
- Total Applications
- Average Security Score
- Security Controls Implementation Rate
- High Risk Applications Count

#### Lifecycle States
- Applications per state
- Average security score per state
- State-specific security controls
- Implementation progress

#### Security Controls
- Overall implementation progress
- Control type breakdown
- Implementation rates
- Visual progress indicators

Access via:
- Click Dashboard tab in navigation bar
- Select Dashboard from user menu
- Navigate to `/dashboard`

### Additional Features
- **Applications Management** (`/applications`)
  - Add/Edit applications
  - Security assessments
  - Risk management
  
- **Reporting** (`/reports`)
  - Generate security reports
  - Export data
  - Compliance documentation

### Authentication
- Secure login system
- JWT token-based authentication
- OAuth/SSO integration ready
- Protected routes and API endpoints

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
flask db upgrade
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Quick Start
1. Start the backend server:
```bash
cd backend
flask run
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the application at http://localhost:3000

## Documentation
Detailed documentation can be found in the [/docs](/docs) directory:
- [API Documentation](/docs/api.md)
- [User Guide](/docs/user-guide.md)
- [Admin Guide](/docs/admin-guide.md)
- [Database Schema](/docs/database.md)
- [Task Queue System](/docs/task-queue.md)

## Contributing
Please read [CONTRIBUTING.md](/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
AppSentinel is open source software licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### Third-Party Licenses

This project uses several open source packages. Major dependencies include:

#### Backend Dependencies
- Flask (BSD-3-Clause)
- SQLAlchemy (MIT)
- Flask-SQLAlchemy (BSD-3-Clause)
- Flask-Migrate (MIT)
- Flask-CORS (MIT)
- psycopg2-binary (LGPL-3.0)
- python-dotenv (BSD-3-Clause)
- boto3 (Apache-2.0)

#### Frontend Dependencies
- React (MIT)
- Material-UI (MIT)
- TypeScript (Apache-2.0)
- Jest (MIT)

For a complete list of dependencies and their licenses, run:
```bash
# Backend licenses
make show-licenses-backend

# Frontend licenses
make show-licenses-frontend
```

### Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

### Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct. By participating, you are expected to uphold this code.
