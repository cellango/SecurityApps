Feature: Navigation Flow
  As a security engineer
  I want to navigate through different views of the application
  So that I can access security information in different ways

  Background:
    Given I am logged in as "admin"
    And the following teams exist:
      | name           | description          |
      | Security Team  | Core security team   |
      | DevOps Team    | Infrastructure team  |
    And the following applications exist:
      | name    | team          | security_score |
      | App1    | Security Team | 85            |
      | App2    | DevOps Team   | 75            |

  Scenario: Navigate from Login to Selection
    When I log in successfully
    Then I should see the selection page
    And I should see two options:
      | option             |
      | View by Team       |
      | View by Application|

  Scenario: Navigate to Team View
    Given I am on the selection page
    When I click "View by Team"
    Then I should see the teams list
    And I should see the following teams:
      | name           | app_count | avg_score |
      | Security Team  | 1         | 85        |
      | DevOps Team    | 1         | 75        |

  Scenario: Navigate to Team's Applications
    Given I am on the teams list
    When I click on "Security Team"
    Then I should see the team's applications page
    And I should see "App1" in the applications list
    And I should not see "App2" in the applications list

  Scenario: Navigate to Applications View
    Given I am on the selection page
    When I click "View by Application"
    Then I should see the applications list
    And I should see all applications:
      | name | team          | score |
      | App1 | Security Team | 85    |
      | App2 | DevOps Team   | 75    |

  Scenario: Navigate to Application Details
    Given I am on the applications list
    When I click on application "App1"
    Then I should see the application details page
    And I should see the security score breakdown
    And I should see the remediation recommendations

  Scenario: Use Back Navigation
    Given I am on the application details page
    When I click the back button
    Then I should return to the applications list
    When I click the back button again
    Then I should return to the selection page

  Scenario: Use Home Navigation
    Given I am on the application details page
    When I click on the user menu
    And I click "Home"
    Then I should return to the selection page

  Scenario: Breadcrumb Navigation
    Given I am viewing "App1" details from the team view
    Then I should see the breadcrumb trail:
      | level    | text          |
      | 1        | Teams         |
      | 2        | Security Team |
      | 3        | App1          |
