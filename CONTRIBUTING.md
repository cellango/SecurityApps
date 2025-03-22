# Contributing to SecurityApps

🎉 First off, thanks for taking the time to contribute! 🎉

SecurityApps is a work in progress, and we welcome contributions from the community. This document provides guidelines and information about contributing to this project.

## Project Status

⚠️ **Work in Progress**: This project is actively under development. While the core functionality is implemented, we're continuously improving and adding new features.

## Components

SecurityApps consists of three main components:

1. **AppSentinel**
   - AppScore: Application security scoring system
   - AppInventory: Application inventory management system

2. **PerimeterAI**
   - Enhanced Keycloak with multi-tenancy
   - Keyboard Dynamics-based MFA
   - Policy Studio
   - Digital Signatures (based on EJBCA)
   - Monitoring Component

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker
- Describe what you expected to happen
- Describe what actually happened
- Include steps to reproduce if possible
- Include version information

### Submitting Changes
1. Fork the repository
2. Create a new branch for your changes
3. Make your changes
4. Write or update tests as needed
5. Update documentation as needed
6. Submit a pull request

### Pull Request Process
1. Ensure your code follows the project's coding standards
2. Update the README.md with details of changes if needed
3. Add tests for new functionality
4. Update documentation as needed
5. The PR will be merged once you have the sign-off of at least one maintainer

## Development Setup

Each component has its own setup instructions in its respective directory. Generally, you'll need:

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Java 17+ (for PerimeterAI components)

## Code Style

- Python: Follow PEP 8
- JavaScript: Use ESLint with provided configuration
- Java: Follow Google Java Style Guide

## Testing

- Write unit tests for new code
- Ensure all tests pass before submitting PR
- Include integration tests where appropriate

## Documentation

- Update documentation for new features
- Include docstrings for Python code
- Document API changes
- Update requirements documentation as needed

## Community

- Be welcoming and inclusive
- Follow our Code of Conduct
- Help others who have questions

## Questions?

Feel free to:
- Open an issue for questions
- Join our community discussions
- Reach out to maintainers

## License

By contributing to SecurityApps, you agree that your contributions will be licensed under the Apache License 2.0.
