Feature: Authentication
  As a user
  I want to authenticate with the system
  So that I can access protected resources

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials:
      | username | password |
      | testuser | testpass |
    Then I should be redirected to the dashboard
    And I should see my username in the navigation bar

  Scenario: Failed login with incorrect password
    Given I am on the login page
    When I enter invalid credentials:
      | username | password     |
      | testuser | wrongpass   |
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  Scenario: Failed login with non-existent user
    Given I am on the login page
    When I enter credentials for a non-existent user:
      | username      | password |
      | nonexistent  | testpass |
    Then I should see an error message "User not found"
    And I should remain on the login page

  Scenario: Logout
    Given I am logged in as a user
    When I click the logout button
    Then I should be redirected to the login page
    And I should not be able to access protected resources

  Scenario: Session expiry
    Given I am logged in as a user
    When my session expires
    And I try to access a protected resource
    Then I should be redirected to the login page
    And I should see a message "Session expired. Please log in again"
