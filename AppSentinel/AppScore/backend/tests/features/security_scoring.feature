Feature: Security Scoring
  As a security assessor
  I want to evaluate and track application security scores
  So that I can monitor security posture over time

  Scenario: Create a new security assessment
    Given I am logged in as a security assessor
    When I create a new security assessment for application "Test App" with the following scores:
      | category      | metric           | score | max_score |
      | Authentication| Password Policy  | 4     | 5         |
      | Authorization | Role Management  | 3     | 5         |
      | Data Security| Encryption       | 5     | 5         |
    Then the security score should be calculated correctly
    And the assessment should be saved successfully

  Scenario: View security score history
    Given there is an application with multiple security assessments
    When I view the security score history
    Then I should see a list of all assessments
    And the scores should be displayed in chronological order

  Scenario: Update security assessment
    Given there is an existing security assessment
    When I update the following scores:
      | category      | metric           | new_score |
      | Authentication| Password Policy  | 5         |
    Then the total score should be recalculated
    And an audit log should be created for the change
