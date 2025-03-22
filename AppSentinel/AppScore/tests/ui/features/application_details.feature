Feature: Application Details Page
    As a security analyst
    I want to view application security details
    So that I can assess the security status of applications

    Background:
        Given I am logged in as a security analyst
        And I am on the application details page for application "Test App"

    Scenario: View Application Security Score
        Then I should see the security score displayed
        And the score should be between 0 and 100
        And I should see the last scored date

    Scenario: View Security Findings
        When I click on the "Security Findings" tab
        Then I should see a list of security findings
        And each finding should display severity level
        And each finding should display discovery date

    Scenario: View Compliance Status
        When I click on the "Compliance" tab
        Then I should see the compliance status
        And I should see a list of compliance checks
        And each check should show pass/fail status

    Scenario: Filter Security Findings
        When I click on the "Security Findings" tab
        And I select severity "Critical" from the filter
        Then I should only see findings with "Critical" severity
        
    Scenario: View Historical Scores
        When I click on the "History" tab
        Then I should see a graph of historical scores
        And I should see score trends over time
