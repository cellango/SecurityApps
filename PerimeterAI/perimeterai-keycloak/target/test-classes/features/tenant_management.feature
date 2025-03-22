@tenant
Feature: Tenant Management
  As an administrator
  I want to manage tenants in Keycloak
  So that I can organize and control access for different organizations

  Background:
    Given I am logged in as an administrator
    And I am on the admin console page

  Scenario: View Tenant Management Tab
    Then I should see the "Tenant Management" tab in the navigation menu

  Scenario: Access Tenant Management Page
    When I click on the "Tenant Management" tab
    Then I should be redirected to the tenant management page
    And I should see the tenant list table
    And I should see the "Create Tenant" button

  Scenario: Create New Tenant
    Given I am on the tenant management page
    When I click on the "Create Tenant" button
    Then I should see the tenant creation form
    When I fill in the following tenant details:
      | Name        | Test Tenant      |
      | ID          | test-tenant      |
      | Description | Test Description |
    And I click the "Save" button
    Then I should see a success message
    And I should see "Test Tenant" in the tenant list

  Scenario: Edit Existing Tenant
    Given I am on the tenant management page
    And there is an existing tenant "Test Tenant"
    When I click the edit button for "Test Tenant"
    Then I should see the tenant edit form
    When I update the description to "Updated Description"
    And I click the "Save" button
    Then I should see a success message
    And I should see "Updated Description" in the tenant details

  Scenario: Delete Tenant
    Given I am on the tenant management page
    And there is an existing tenant "Test Tenant"
    When I click the delete button for "Test Tenant"
    Then I should see a confirmation dialog
    When I confirm the deletion
    Then I should see a success message
    And "Test Tenant" should not be in the tenant list
