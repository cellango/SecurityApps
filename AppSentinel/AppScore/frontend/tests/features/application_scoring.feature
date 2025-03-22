Feature: Application Security Scoring
  As a security engineer
  I want to view and manage application security scores
  So that I can track and improve application security

  Background:
    Given I am logged in as a security engineer
    And there are test applications in the system
      | name | description          |
      | App1 | Test Application 1   |
      | App2 | Test Application 2   |

  Scenario: View Application List
    When I visit the application list page
    Then I should see the following applications
      | name | description          |
      | App1 | Test Application 1   |
      | App2 | Test Application 2   |
    And each application should display its current security score

  Scenario: View Application Details
    When I click on application "App1"
    Then I should see the application details page
    And I should see the security score breakdown
      | score_type    | value |
      | Rules Score   | 90    |
      | ML Score      | 85    |
      | Final Score   | 88.5  |
    And I should see the remediation recommendations

  Scenario: Filter Applications by Team
    When I visit the application list page
    And I select team "Security Team"
    Then I should only see applications for "Security Team"

  Scenario: View Score History
    When I click on application "App1"
    And I click on "View Score History"
    Then I should see a chart of historical scores
    And I should see at least 5 historical data points

  Scenario: View Remediation Details
    When I click on application "App1"
    And I click on "View Remediations"
    Then I should see a list of remediation items
    And each remediation should have
      | field       |
      | Title       |
      | Description |
      | Severity    |
      | Effort      |

  Scenario: Sort Applications by Score
    When I visit the application list page
    And I click on "Score" column header
    Then applications should be sorted by score in descending order

  Scenario: Search for Applications
    When I visit the application list page
    And I enter "App" in the search box
    Then I should see applications containing "App"
    And I should not see unmatched applications
