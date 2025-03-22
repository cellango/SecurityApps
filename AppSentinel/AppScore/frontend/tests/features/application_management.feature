Feature: Application Management
  As a security engineer
  I want to manage and view application security details
  So that I can monitor and improve application security

  Background:
    Given I am logged in as "admin"
    And the following applications exist:
      | name    | team          | security_score | critical_vulns | high_vulns |
      | App1    | Security Team | 85            | 0              | 2          |
      | App2    | DevOps Team   | 75            | 1              | 3          |

  Scenario: View Application Security Score
    When I view application "App1"
    Then I should see the following score breakdown:
      | score_type    | value |
      | Rules Score   | 88    |
      | ML Score      | 82    |
      | Final Score   | 85    |
    And I should see a score history chart
    And I should see the scoring factors:
      | factor              | status    |
      | Critical Vulns      | Pass      |
      | High Vulns          | Warning   |
      | Code Coverage       | Pass      |

  Scenario: View Application Remediations
    When I view application "App2"
    Then I should see the following remediations:
      | title                   | severity | effort |
      | Fix Critical Vuln       | High     | Medium |
      | Update Dependencies     | Medium   | Low    |
    And each remediation should have:
      | field                   |
      | Description            |
      | Expected Impact        |
      | Implementation Steps   |

  Scenario: Filter Applications by Score Range
    Given I am on the applications list
    When I set the minimum score filter to "80"
    Then I should only see "App1" in the list
    And I should not see "App2" in the list

  Scenario: Sort Applications
    Given I am on the applications list
    When I click the "Security Score" column header
    Then the applications should be sorted by score in descending order
    When I click the "Security Score" column header again
    Then the applications should be sorted by score in ascending order

  Scenario: Search Applications
    Given I am on the applications list
    When I enter "App" in the search box
    Then I should see both applications
    When I enter "App1" in the search box
    Then I should only see "App1" in the list

  Scenario: View Historical Score Trends
    When I view application "App1"
    And I click on "View Score History"
    Then I should see a chart showing score trends
    And I should see score changes over time:
      | date       | score |
      | 2024-12-01 | 80    |
      | 2024-12-15 | 83    |
      | 2024-12-26 | 85    |

  Scenario: Export Application Report
    When I view application "App1"
    And I click "Export Report"
    Then a PDF should be downloaded containing:
      | section             |
      | Score Breakdown     |
      | Vulnerabilities     |
      | Remediation Items   |
      | Historical Trends   |

  Scenario: View Team Security Overview
    When I view team "Security Team"
    Then I should see the team's security dashboard
    And I should see the following metrics:
      | metric                  | value |
      | Average Score          | 85    |
      | Critical Findings      | 0     |
      | High Findings          | 2     |
      | Applications at Risk   | 0     |
