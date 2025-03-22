Feature: Export Filter Presets
  As a user
  I want to save and manage export filter presets
  So that I can quickly apply commonly used filter combinations

  Background:
    Given I am on the dashboard page
    And the following departments exist:
      | name          |
      | Engineering   |
      | IT Security   |
      | Compliance    |
    And the following teams exist:
      | name          |
      | Frontend      |
      | Backend       |
      | DevOps        |

  Scenario: View filter suggestions
    When I click the "Export with Filters" button
    Then I should see department suggestions including:
      | Engineering   |
      | IT Security   |
      | Compliance    |
    And I should see team suggestions including:
      | Frontend      |
      | Backend       |
      | DevOps        |
    And I should see all control family options
    And I should see all implementation status options

  Scenario: Create a new filter preset
    When I click the "Export with Filters" button
    And I select "Engineering" from department suggestions
    And I select "Frontend" from team suggestions
    And I select "ACCESS_CONTROL" from control families
    And I select "IMPLEMENTED" from implementation status
    And I click "Save as Preset"
    And I enter "Engineering Frontend Controls" as preset name
    And I click "Save"
    Then I should see "Engineering Frontend Controls" in the presets list
    And the preset should show the correct filter values

  Scenario: Apply a saved preset
    Given I have a saved preset "Engineering Frontend Controls"
    When I click the "Export with Filters" button
    And I click the use preset button for "Engineering Frontend Controls"
    Then the department field should show "Engineering"
    And the team field should show "Frontend"
    And the control family field should show "ACCESS_CONTROL"
    And the implementation status field should show "IMPLEMENTED"

  Scenario: Delete a filter preset
    Given I have a saved preset "Engineering Frontend Controls"
    When I click the "Export with Filters" button
    And I click the delete button for "Engineering Frontend Controls"
    Then I should not see "Engineering Frontend Controls" in the presets list

  Scenario: Export with applied filters
    Given I have a saved preset "Engineering Frontend Controls"
    When I click the "Export with Filters" button
    And I click the use preset button for "Engineering Frontend Controls"
    And I click "Export Excel"
    Then the Excel file should be downloaded
    And the Excel file should contain filtered data for:
      | Department  | Team     | Control Family  | Status      |
      | Engineering | Frontend | ACCESS_CONTROL  | IMPLEMENTED |
