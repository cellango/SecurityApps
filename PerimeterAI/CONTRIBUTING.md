# Contributing to PerimeterAI

We love your input! We want to make contributing to PerimeterAI as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Components

### perimeterai-signature
The core digital signature service based on EJBCA. When contributing to this component:
- Follow EJBCA coding standards
- Include appropriate unit tests
- Update documentation for any API changes
- Test against PostgreSQL database

### perimeterai-keycloak
Custom Keycloak implementation. When contributing to this component:
- Follow Keycloak theme development guidelines
- Test all UI changes across different browsers
- Update translation files if adding new text
- Test tenant management features

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Any contributions you make will be under the AGPL-3.0 Software License
In short, when you submit code changes, your submissions are understood to be under the same [AGPL-3.0 License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issue tracker]
We use GitHub issues to track public bugs. Report a bug by [opening a new issue]().

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License
By contributing, you agree that your contributions will be licensed under its AGPL-3.0 License.
