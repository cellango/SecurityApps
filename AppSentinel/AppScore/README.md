# Security Score Card

A comprehensive application security scoring system that combines rules-based evaluation with machine learning to provide actionable security insights.

# AppInventory

> **Development Version 0.9.0**
> ⚠️ This application is currently under active development.

## Authors

- **Clement Ellango** - *Lead Developer* - Security Architecture and Backend Development
- **Carolina Clement** - *Lead Developer* - Frontend Development and Security Engineering

## Features

### 1. Security Scoring
- Hybrid scoring system combining rules and machine learning
- Real-time security assessment
- Historical score tracking
- Customizable scoring weights (default: 70% rules, 30% ML)

### 2. Application Management
- Integration with application catalog
- Team-based access control
- Application grouping and filtering
- Automatic synchronization with external catalogs
- Advanced search and filtering capabilities
- Historical trend analysis
- Export functionality for reports

### 3. Security Tools Integration
- Snyk vulnerability scanning
- SonarQube code analysis
- Black Duck software composition analysis
- Veracode static analysis
- Extensible integration framework

### 4. Machine Learning Capabilities
- Automated score prediction
- Pattern detection
- Model versioning
- Training history tracking
- Feature importance analysis

### 5. Remediation Management
- Prioritized recommendations
- Effort estimation
- Progress tracking
- Impact assessment
- Historical improvement analysis

### 6. Authentication & Authorization
- Secure JWT-based authentication
- Role-based access control
- Session management
- Password hashing with bcrypt
- Protected API endpoints

### 7. User Interface
- Modern Material-UI components
- Responsive design
- Intuitive navigation
- Team and application views
- Interactive dashboards
- Breadcrumb navigation

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Node.js 14+
- AWS Account (for production deployment)

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd SecurityScoreCard
```

2. Set up environment files:
```bash
# Copy example environment files
cp .env.example .env
cp backend/.secrets.json.example backend/.secrets.json
```

3. Build and start the containers:
```bash
docker-compose up -d --build
```

4. Access the application:
- Frontend: http://localhost:3001
- Backend API: http://localhost:5001

## Production Deployment

### AWS Secrets Manager Setup

1. Install AWS CLI and configure credentials:
```bash
aws configure
```

2. Create required secrets in AWS Secrets Manager:
```bash
# Create database password secret
aws secretsmanager create-secret \
    --name prod/security-score-card/db-password \
    --description "Database password for Security Score Card" \
    --secret-string "your-secure-password"

# Create application secret key
aws secretsmanager create-secret \
    --name prod/security-score-card/secret-key \
    --description "Flask application secret key" \
    --secret-string "your-secure-secret-key"

# Create JWT secret key
aws secretsmanager create-secret \
    --name prod/security-score-card/jwt-secret-key \
    --description "JWT authentication secret key" \
    --secret-string "your-secure-jwt-secret"
```

3. Set up IAM Role/User:
   - Create an IAM role with the following policy:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "secretsmanager:GetSecretValue"
               ],
               "Resource": [
                   "arn:aws:secretsmanager:*:*:secret:prod/security-score-card/*"
               ]
           }
       ]
   }
   ```
   - Attach this role to your production EC2 instances or ECS tasks

4. Configure production environment:
   - Create `.env.production` with appropriate values:
   ```
   FLASK_ENV=production
   AWS_REGION=your-aws-region
   DB_HOST=your-production-db-host
   DB_PORT=5432
   DB_NAME=security_score_card
   DB_USER=your-production-db-user
   LOG_LEVEL=WARNING
   ```

### Production Deployment Steps

1. Build production images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Deploy to your production environment:
   - Push images to ECR/Docker registry
   - Deploy using your preferred orchestration tool (ECS, Kubernetes, etc.)
   - Ensure AWS credentials are properly configured
   - Verify secrets are accessible

## Security Considerations

1. Secrets Management:
   - Never commit `.env` or `.secrets.json` files
   - Use AWS Secrets Manager in production
   - Rotate secrets regularly
   - Use least-privilege IAM roles

2. Database:
   - Use strong passwords
   - Restrict database access to application servers
   - Regular backups
   - Encrypt data at rest

3. Application:
   - Keep dependencies updated
   - Regular security audits
   - Monitor application logs
   - Enable AWS CloudTrail for API activity monitoring

## Getting Started

### Prerequisites
```bash
# Python 3.8+
python --version

# Node.js 14+
node --version

# PostgreSQL 12+
postgres --version

# Docker (optional, for containerized database)
docker --version
```

### Environment Variables
```bash
# Application Settings
APP_CATALOG_API_URL=https://your-catalog-api.com
APP_CATALOG_API_KEY=your-api-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/security_score_card
SECRET_KEY=your-secret-key

# Security Tool API Keys
SNYK_API_KEY=your-snyk-key
SONARQUBE_API_KEY=your-sonar-key
SONARQUBE_URL=http://localhost:9000
BLACKDUCK_API_KEY=your-blackduck-key
BLACKDUCK_URL=your-blackduck-url
VERACODE_API_KEY=your-veracode-key
VERACODE_API_SECRET=your-veracode-secret
```

### Installation

1. Database Setup (Docker)
```bash
# Start PostgreSQL container
docker-compose up -d
```

2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
cd backend
alembic upgrade head

# Initialize database and create admin user
python backend/scripts/init_db.py
python backend/scripts/create_admin.py
```

3. Frontend Setup
```bash
cd frontend
npm install
```

### Running the Application

1. Start Backend
```bash
cd backend
python app.py
```

2. Start Frontend
```bash
cd frontend
npm start
```

3. Access the Application
- Open http://localhost:3001 in your browser
- Log in with:
  - Username: admin
  - Password: admin

## Docker Setup

### Building the Application
```bash
# Build all services
docker compose build

# Build specific service
docker compose build backend
docker compose build frontend
```

### Running with Docker
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Docker Services
1. **Frontend** (http://localhost:3001)
   - React application
   - Served by Nginx
   - Automatic hot-reloading in development

2. **Backend** (http://localhost:5000)
   - Flask API
   - Automatic database migrations
   - Creates admin user on first run

3. **PostgreSQL** (localhost:5433)
   - Persistent data storage
   - Automatic health checks
   - Volume mounted for data persistence

### Development with Docker
1. Start services:
```bash
docker compose up -d
```

2. View logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
```

3. Execute commands:
```bash
# Backend commands
docker compose exec backend python scripts/create_admin.py

# Database commands
docker compose exec postgres psql -U postgres -d security_score_card
```

4. Rebuild after changes:
```bash
docker compose build
docker compose up -d
```

## Testing

### Running Tests

1. Backend Tests
```bash
cd backend
pytest
```

2. Frontend Tests
```bash
cd frontend
npm test
```

3. BDD Tests
```bash
cd frontend
npm run test:e2e
```

### Test Coverage

The application includes comprehensive test coverage:

1. Unit Tests
- Backend API endpoints
- Database models
- Authentication services
- Security scoring logic

2. Integration Tests
- API integration tests
- Database integration tests
- External service mocking

3. BDD Tests
- Authentication flows
- Navigation paths
- Application management
- Team management
- Security score visualization
- Report generation

### Test Documentation

Detailed test scenarios are available in:
- `/frontend/tests/features/*.feature` - BDD feature specifications
- `/frontend/tests/features/steps/*.py` - Step definitions
- `/backend/tests/` - Backend test suites

## Architecture

### Frontend
- React.js with Material-UI
- Redux for state management
- Axios for API communication
- JWT for authentication
- React Router for navigation

### Backend
- Flask REST API
- SQLAlchemy ORM
- JWT authentication
- PostgreSQL database
- Bcrypt password hashing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
