Feature: Dashboard
  As a user
  I want to view the application dashboard
  So that I can get an overview of all applications and their status

  Background:
    Given I am logged in as a user
    And the following applications exist:
      | name           | state       | application_type | department_name |
      | Frontend App   | PRODUCTION  | WEB             | Engineering     |
      | Backend API    | DEVELOPMENT | API             | Engineering     |
      | Security Tool  | TESTING     | TOOL            | IT Security     |

  Scenario: View application statistics
    When I visit the dashboard page
    Then I should see the total number of applications
    And I should see applications by state:
      | state       | count |
      | PRODUCTION  | 1     |
      | DEVELOPMENT | 1     |
      | TESTING     | 1     |
    And I should see applications by type:
      | type | count |
      | WEB  | 1     |
      | API  | 1     |
      | TOOL | 1     |

  Scenario: Filter applications by department
    When I select department "Engineering"
    Then I should see 2 applications
    And I should see "Frontend App"
    And I should see "Backend API"
    And I should not see "Security Tool"

  Scenario: Filter applications by state
    When I select state "PRODUCTION"
    Then I should see 1 application
    And I should see "Frontend App"
    And I should not see "Backend API"
    And I should not see "Security Tool"

  Scenario: Sort applications by name
    When I click the "Name" column header
    Then the applications should be sorted alphabetically
    And "Backend API" should appear before "Frontend App"

  Scenario: Export dashboard data
    When I click the "Export" button
    And I select format "CSV"
    Then a CSV file should be downloaded
    And it should contain all visible application data
