# UI Testing with Selenium and Behave

This directory contains BDD-style UI tests for the Security Score Card application using Selenium WebDriver and Behave.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Chrome browser is installed (the tests use ChromeDriver)

## Running Tests

1. Start the application:
```bash
# From the root directory
docker-compose up
```

2. Run the tests:
```bash
# From the tests/ui directory
behave features/
```

To run specific features:
```bash
behave features/application_details.feature
```

## Test Reports

- Screenshots of failed steps are automatically saved in the current directory
- For HTML reports, you can use allure-behave:
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/ features/
allure serve reports/
```

## Directory Structure

```
ui/
├── features/
│   ├── application_details.feature    # Feature files
│   ├── steps/
│   │   └── application_details_steps.py   # Step definitions
│   └── environment.py                # Test environment setup
├── requirements.txt                  # Python dependencies
└── README.md                        # This file
```

## Adding New Tests

1. Create a new feature file in `features/`
2. Add corresponding step definitions in `features/steps/`
3. Update environment.py if needed for new setup/teardown requirements

## Best Practices

- Keep features focused and scenarios independent
- Use clear, descriptive step names
- Add appropriate waits for dynamic elements
- Take screenshots on failures
- Use page objects for complex pages
- Keep locators maintainable and unique
