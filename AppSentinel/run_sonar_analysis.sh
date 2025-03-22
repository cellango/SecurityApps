#!/bin/bash

# Function to wait for SonarQube to be ready
wait_for_sonarqube() {
    echo "Waiting for SonarQube to be ready..."
    while ! curl -s http://localhost:9000/api/system/status | grep -q '"status":"UP"'; do
        sleep 5
    done
    echo "SonarQube is ready!"
}

# Run tests for each application
run_app_tests() {
    local app_name=$1
    echo "Running tests for $app_name..."
    cd $app_name
    ./run_tests.sh
    cd ..
}

# Run SonarQube analysis for each application
run_sonar_analysis() {
    local app_name=$1
    echo "Running SonarQube analysis for $app_name..."
    cd $app_name
    sonar-scanner
    cd ..
}

# Main execution
echo "Starting AppSentinel test and analysis suite..."

# Ensure SonarQube is ready
wait_for_sonarqube

# Run tests and analysis for each application
for app in AppInventory AppScore; do
    run_app_tests $app
    run_sonar_analysis $app
done

echo "All tests and analysis completed. Check SonarQube dashboard at http://localhost:9000"
