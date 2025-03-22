docker compose up -d# AppSentinel: Application Security Management Suite

AppSentinel is a comprehensive suite of applications designed to streamline and enhance Application Security operations within cybersecurity teams. This platform provides tools for managing application inventory, security controls, risk assessments, and security scoring.

## Authors

- **Clement Ellango** - *Lead Developer* - Security Architecture and Backend Development
- **Carolina Clement** - *Lead Developer* - Frontend Development and Security Engineering

## Applications

### 1. AppInventory
A centralized application inventory management system that helps security teams track and manage all applications within their organization.

**Key Features:**
- Application metadata management
- Security controls tracking
- Audit logging with Jira integration
- Risk assessment tracking
- Security review scheduling
- Export and reporting capabilities

### 2. AppScore
A security scoring and assessment platform that helps evaluate and track the security posture of applications.

**Key Features:**
- Security scoring framework
- Compliance tracking
- Risk assessment
- Security metrics dashboard
- Trend analysis
- Recommendation engine

## Navigation Structure

AppSentinel provides a user-friendly navigation system:

### Main Navigation
- **Home (Landing Page)** - `/`
  - Overview of AppSentinel
  - Quick access to key features
  - Available via:
    - AppSentinel logo click
    - Home tab in navigation bar
    - User menu dropdown
    - Direct URL: `/`

- **Dashboard** - `/dashboard`
  - Comprehensive application security metrics
  - Lifecycle state analysis
  - Security controls implementation status
  - Recent activity feed
  - Available via:
    - Dashboard tab in navigation bar
    - User menu dropdown
    - Direct URL: `/dashboard`

- **Applications** - `/applications`
  - Application inventory management
  - Security assessment tools
  - Risk analysis

- **Reports** - `/reports`
  - Security reporting
  - Compliance documentation
  - Audit trails

### Authentication Pages
- **Login** - `/login`
  - User authentication
  - OAuth/SSO options
  - Secure session management

### User Menu
Access additional options through the user menu (top-right):
- Profile settings
- Quick navigation to Home/Dashboard
- Logout option

## Authentication

AppSentinel provides enterprise-grade authentication using both OAuth/OIDC and SAML protocols, powered by Keycloak. This enables:

- Single Sign-On (SSO) across all AppSentinel applications
- Role-Based Access Control (RBAC)
- Support for both OAuth/OIDC and SAML authentication
- Enterprise IdP integration

For detailed information:
- [Authentication Documentation](docs/authentication.md)
- [Authentication Quick Start Guide](docs/quickstart-auth.md)

## Technology Stack

- **Frontend**: React.js with Material-UI
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest, Behave, Selenium
- **Quality Assurance**: SonarQube

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd AppSentinel
```

2. Start all services:
```bash
docker compose up --build
```

### Accessing the Applications

- **AppInventory**:
  - Frontend: http://localhost:3000
  - API: http://localhost:5000
  - Database: appinventory

- **AppScore**:
  - Frontend: http://localhost:3001
  - API: http://localhost:5001
  - Database: appscore

- **SonarQube**:
  - Dashboard: http://localhost:9000
  - Default credentials: admin/admin

## Testing

AppSentinel implements a comprehensive testing strategy including:

### Unit Tests
- Backend unit tests using pytest
- Frontend unit tests using Jest
- Code coverage reports

### BDD Tests
- Behavior-driven development tests using Behave
- Feature files describing application behavior
- Step definitions implementing test scenarios

### End-to-End Tests
- Selenium WebDriver for browser automation
- Integration with Selenium Grid for parallel testing
- Cross-browser testing capabilities

### Running Tests

Each application has its own test suite. To run tests:

```bash
# For AppInventory
cd AppInventory
./run_tests.sh

# For AppScore
cd AppScore
./run_tests.sh
```

### Test Reports
- Test results are available in `test-reports` directory
- Coverage reports are generated in HTML and XML formats
- SonarQube dashboard shows detailed code quality metrics

## Architecture

### Shared Infrastructure
- Single PostgreSQL instance serving all applications
- Docker network for secure inter-service communication
- Shared authentication and authorization
- Centralized test reporting through SonarQube

### Development Features
- Hot-reloading for rapid development
- Volume mounts for live code updates
- Environment-based configuration
- Health checks for dependencies

## Contributing

We welcome contributions to AppSentinel! Please read our contributing guidelines for details on our code of conduct and the process for submitting pull requests.

### Development Workflow
1. Write tests first (TDD/BDD approach)
2. Implement features
3. Ensure all tests pass
4. Check SonarQube for code quality issues
5. Submit pull request

## Future Applications

We plan to expand the AppSentinel suite with additional tools:

1. **AppScan**: Automated security scanning orchestration
2. **AppVuln**: Vulnerability management system
3. **AppPolicy**: Security policy management and compliance tracking

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the security team.
