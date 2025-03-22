Feature: Authentication
  As a security engineer
  I want to securely log in to the application
  So that I can access the security scoring system

  Background:
    Given the database is clean
    And there is an admin user in the system
      | username | password | email           |
      | admin    | admin    | admin@test.com  |

  Scenario: Successful Login
    When I visit the login page
    And I enter "admin" as username
    And I enter "admin" as password
    And I click the "Sign In" button
    Then I should be redirected to the selection page
    And I should see "Welcome to Security Score Card" on the page
    And the JWT token should be stored in localStorage

  Scenario: Failed Login - Wrong Password
    When I visit the login page
    And I enter "admin" as username
    And I enter "wrong_password" as password
    And I click the "Sign In" button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page
    And no JWT token should be stored

  Scenario: Failed Login - Non-existent User
    When I visit the login page
    And I enter "non_existent" as username
    And I enter "password" as password
    And I click the "Sign In" button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  Scenario: Logout
    Given I am logged in as "admin"
    When I click on the user menu
    And I click "Sign Out"
    Then I should be redirected to the login page
    And the JWT token should be removed from localStorage

  Scenario: Access Protected Route Without Authentication
    When I try to visit the "/applications" page directly
    Then I should be redirected to the login page
    And I should see a message "Please log in to continue"

  Scenario: Session Persistence
    Given I am logged in as "admin"
    When I refresh the page
    Then I should remain logged in
    And I should see the same page I was on
