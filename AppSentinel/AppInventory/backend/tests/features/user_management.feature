Feature: User Management
  As an administrator
  I want to manage user accounts
  So that I can control access to the system

  Background:
    Given I am logged in as an administrator
    And the following users exist:
      | username | role    | department    |
      | user1    | USER    | Engineering   |
      | user2    | ADMIN   | IT Security   |
      | user3    | USER    | Compliance    |

  Scenario: Create new user
    When I navigate to user management
    And I create a new user with details:
      | username | password  | role | department  |
      | newuser  | pass123   | USER | Engineering |
    Then the user should be created successfully
    And I should see "newuser" in the users list
    And an audit log should be created for the user creation

  Scenario: Update user role
    When I navigate to user management
    And I select user "user1"
    And I change their role to "ADMIN"
    Then the user's role should be updated
    And I should see "user1" with role "ADMIN"
    And an audit log should be created for the role change

  Scenario: Disable user account
    When I navigate to user management
    And I select user "user3"
    And I disable their account
    Then the user's account should be disabled
    And I should see "user3" marked as disabled
    And an audit log should be created for the account disable

  Scenario: Filter users by department
    When I navigate to user management
    And I filter by department "Engineering"
    Then I should see "user1"
    And I should not see "user2"
    And I should not see "user3"

  Scenario: Search users
    When I navigate to user management
    And I search for "user"
    Then I should see all users in the results
    And the results should be sorted by username
