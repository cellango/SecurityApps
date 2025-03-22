# Testing Documentation

## Overview

The Security Score Card application implements a comprehensive testing strategy that includes unit tests, integration tests, and behavior-driven development (BDD) tests. This ensures high code quality, maintainability, and reliability of the application.

## Test Structure

### 1. BDD Tests (`/frontend/tests/features/`)

#### Feature Files
- `auth.feature`: Authentication scenarios
- `navigation.feature`: Navigation flow tests
- `application_management.feature`: Application-specific features

#### Step Definitions (`/frontend/tests/features/steps/`)
- `auth_steps.py`: Authentication step implementations
- `navigation_steps.py`: Navigation step implementations
- `application_steps.py`: Application management step implementations

### 2. Unit Tests

#### Backend (`/backend/tests/`)
- API endpoint tests
- Model tests
- Service tests
- Utility function tests

#### Frontend (`/frontend/src/__tests__/`)
- Component tests
- Redux action/reducer tests
- Utility function tests
- Hook tests

## Running Tests

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL (running on port 5433)
- Chrome/Firefox WebDriver for BDD tests

### Backend Tests
```bash
cd backend
pytest                 # Run all tests
pytest -v              # Verbose output
pytest -k "test_name"  # Run specific test
pytest --cov          # Run with coverage
```

### Frontend Tests
```bash
cd frontend
npm test              # Run all tests
npm test -- --watch   # Watch mode
npm test -- -t "test name"  # Run specific test
```

### BDD Tests
```bash
cd frontend
npm run test:e2e           # Run all BDD tests
npm run test:e2e -- --tags @auth  # Run auth scenarios only
```

## Test Categories

### 1. Authentication Tests
- Login success/failure scenarios
- Token management
- Session handling
- Protected route access
- Logout functionality

### 2. Navigation Tests
- Menu navigation
- Breadcrumb functionality
- Back button behavior
- View switching
- Deep linking

### 3. Application Management Tests
- Application listing
- Filtering and sorting
- Score visualization
- Report generation
- Historical trends

### 4. Integration Tests
- API endpoint integration
- Database operations
- External service mocking
- Error handling

## Writing Tests

### BDD Test Guidelines
1. Use descriptive feature names
2. Write scenarios from user perspective
3. Keep steps atomic and reusable
4. Use tables for data-driven tests
5. Tag scenarios appropriately

Example:
```gherkin
Feature: Application Filtering
  As a security engineer
  I want to filter applications by score
  So that I can focus on high-risk applications

  @filtering @score
  Scenario: Filter by minimum score
    Given I am logged in as "admin"
    And I am on the applications page
    When I set minimum score to "80"
    Then I should only see applications with score >= 80
```

### Unit Test Guidelines
1. Follow AAA pattern (Arrange, Act, Assert)
2. Use meaningful test names
3. Test edge cases
4. Mock external dependencies
5. Keep tests independent

Example:
```python
def test_application_score_calculation():
    # Arrange
    app = Application(name="Test App")
    vulnerabilities = [
        Vulnerability(severity="high", count=2),
        Vulnerability(severity="medium", count=3)
    ]
    
    # Act
    score = calculate_security_score(app, vulnerabilities)
    
    # Assert
    assert score == 75  # Based on scoring algorithm
```

## Test Coverage

### Current Coverage Targets
- Backend: 90% line coverage
- Frontend: 85% line coverage
- Critical paths: 100% coverage

### Coverage Reports
- Backend: Generated with pytest-cov
- Frontend: Generated with Jest
- BDD: Cucumber reports

## Continuous Integration

### GitHub Actions Workflow
1. Run unit tests
2. Run integration tests
3. Run BDD tests
4. Generate coverage reports
5. Deploy if all tests pass

### Quality Gates
- All tests must pass
- Coverage must meet targets
- No security vulnerabilities
- Code style checks pass

## Troubleshooting

### Common Issues

1. WebDriver Issues
```bash
# Update WebDriver
webdriver-manager update
```

2. Database Connection
```bash
# Ensure PostgreSQL is running
docker-compose ps
```

3. Test Timeouts
- Increase timeout in `jest.config.js`
- Check for slow operations
- Verify test data setup

### Debug Tools
- Browser DevTools for BDD tests
- pytest --pdb for Python tests
- Jest --debug for JavaScript tests

## Contributing

### Adding New Tests
1. Identify test category
2. Write test cases
3. Implement tests
4. Update documentation
5. Submit pull request

### Code Review Checklist
- [ ] Tests follow guidelines
- [ ] Coverage is maintained
- [ ] Documentation is updated
- [ ] No flaky tests
- [ ] Performance impact considered
