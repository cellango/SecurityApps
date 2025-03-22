Feature: Application Search
  As a user
  I want to search for applications
  So that I can quickly find and access application information

  Background:
    Given I am logged in as a user
    And the following applications exist:
      | name           | description                | department_name | team_name |
      | Frontend App   | Customer facing app        | Engineering    | Frontend  |
      | Backend API    | Internal API service       | Engineering    | Backend   |
      | Security Tool  | Security scanning tool     | IT Security    | DevOps    |

  Scenario: Search by application name
    When I type "Front" in the search box
    Then I should see "Frontend App" in the search results
    And I should not see "Backend API" in the search results

  Scenario: Search by department
    When I type "Security" in the search box
    Then I should see "Security Tool" in the search results
    And the result should show "IT Security" as the department

  Scenario: Search with no results
    When I type "NonExistent" in the search box
    Then I should see "No applications found" message
    And the search results should be empty

  Scenario: Search without authentication
    Given I am not logged in
    When I type "App" in the search box
    Then I should see "Please log in to search applications" message

  Scenario: Search with expired session
    Given my session has expired
    When I type "App" in the search box
    Then I should see "Session expired. Please log in again" message
