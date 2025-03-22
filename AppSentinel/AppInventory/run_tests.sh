#!/bin/bash

# Run unit tests with coverage
echo "Running unit tests..."
pytest tests/unit --cov=app --cov-report=xml --cov-report=html

# Run BDD tests
echo "Running BDD tests..."
behave tests/features

# Run frontend tests
echo "Running frontend tests..."
cd frontend && npm test -- --coverage

# Run SonarQube analysis
echo "Running SonarQube analysis..."
sonar-scanner

echo "All tests completed. Check test-reports directory for results."
