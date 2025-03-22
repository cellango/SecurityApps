#!/bin/bash

# Start all services
cd ..
make start

# Wait for Keycloak to be ready
echo "Waiting for Keycloak to start..."
sleep 30

# Install required Python packages
pip install python-keycloak requests

# Run Keycloak setup script
python setup_keycloak.py

echo "Setup complete! You can now access:"
echo "- Keycloak Admin Console: http://localhost:8080/admin (admin/admin)"
echo "- AppInventory Frontend: http://localhost:3000"
echo "- Test user credentials: testuser/testpass"
