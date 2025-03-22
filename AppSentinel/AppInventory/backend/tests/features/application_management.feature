Feature: Application Management
  As a security analyst
  I want to manage applications in the inventory
  So that I can track and monitor application security status

  Scenario: Create a new application
    Given I am logged in as a security analyst
    When I create a new application with the following details:
      | name        | description     | application_type | state        | owner_id |
      | Test App    | Test Description| WEB             | DEVELOPMENT  | user123  |
    Then the application should be created successfully
    And I should see the application in the list

  Scenario: Update application status
    Given there is an existing application "Test App"
    When I update the application state to "PRODUCTION"
    Then the application state should be updated
    And an audit log should be created for the change

  Scenario: View audit logs
    Given there are audit logs in the system
    When I request to view the audit logs
    Then I should see a list of audit logs
    And each log should contain action and timestamp
