#!/bin/bash

# Exit on error
set -e

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-test.txt

# Run tests with coverage
pytest tests/ \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    --verbose

# Deactivate virtual environment
deactivate
