Feature: The promotions service back-end
    As a Marketing Manager
    I need a RESTful catalog service
    So that I can keep track of all promotions

Background:
    Given the following promotions
        | name              | starts_at   | ends_at     | active  |
        | buy_one_get_one   | 2022-06-02  | 2022-06-04  | True    |
        | 10_dollars_off    | 2022-06-01  | 2022-06-03  | True    |
        | 20_percent_off    | 2022-06-02  | 2022-06-03  | True    |
        | free_shipping     | 2022-06-01  | 2022-06-05  | False   |
        | 30_days_free      | 2022-06-01  | 2022-06-03  | True    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Pet
    When I visit the "Home Page"
    And I set the "name" to "50_percent_off"
    And I set the "starts_at" to "06-02-2022"
    And I set the "ends_at" to "06-03-2022"
    And I select "True" in the "active" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "name" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "50_percent_off" in the "name" field
    And I should see "True" in the "active" dropdown
    And I should see "2022-06-02" in the "starts_at" field
    And I should see "2022-06-03" in the "ends_at" field

Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "buy_one_get_one" in the results
    And I should see "10_dollars_off" in the results
    And I should not see "free_shipping" in the results

# Scenario: Search for starts_at
#     When I visit the "Home Page"
#     And I set the "starts_at" to "2022-06-02"
#     And I press the "Search" button
#     Then I should see "buy_one_get_one" in the results
#     And I should not see "10_dollars_off" in the results
#     And I should not see "30_days_free" in the results

Scenario: Search for active promotions
    When I visit the "Home Page"
    And I select "True" in the "Active" dropdown
    And I press the "Search" button
    Then I should see "30_days_free" in the results
    And I should see "buy_one_get_one" in the results
    And I should see "10_dollars_off" in the results
    And I should see "20_percent_off" in the results
    And I should not see "free_shipping" in the results


Scenario: Delete a Promotion
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "30_days_free" in the results
    When I press the "Delete" button
    Then I should see the message "Promotion has been Deleted!"

Scenario: Update a Promotion
    When I visit the "Home Page"
    And I set the "Name" to "10_dollars_off"
    And I press the "Search" button
    Then I should see "10_dollars_off" in the "Name" field
    And I should see "2022-06-01" in the "starts_at" field
    And I should see "2022-06-03" in the "ends_at" field
    When I change "Name" to "20_dollars_off"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "20_dollars_off" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "20_dollars_off" in the results
    And I should not see "10_dollars_off" in the results

Scenario: Inactivate a Promotion
    When I visit the "Home Page"
    And I set the "Name" to "buy_one_get_one"
    And I press the "Search" button
    Then I should see "buy_one_get_one" in the "Name" field
    When I select "False" in the "Active" dropdown
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Search" button
    Then I should see "false" in the results
