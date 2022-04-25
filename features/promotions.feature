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

# Scenario: Create a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "Happy"
#     And I set the "Category" to "Hippo"
#     And I select "False" in the "Available" dropdown
#     And I select "Male" in the "Gender" dropdown
#     And I set the "Birthday" to "06-16-2022"
#     And I press the "Create" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     Then the "Id" field should be empty
#     And the "Name" field should be empty
#     And the "Category" field should be empty
#     When I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see "Happy" in the "Name" field
#     And I should see "Hippo" in the "Category" field
#     And I should see "False" in the "Available" dropdown
#     And I should see "Male" in the "Gender" dropdown
#     And I should see "2022-06-16" in the "Birthday" field

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
    And I set the "name" to "30_days_free "
    And I press the "Search" button
    Then I should see "30_days_free " in the "name" field
    And I should see "2022-06-01" in the "start" field
    When I press the "Delete" button
    Then I should see the message "Promotion has been Deleted!"
    When I press the "Search" button
    Then I should not see "30_days_free" in the results

Scenario: Update a Promotion
    When I visit the "Home Page"
    And I set the "name" to "10_dollars_off"
    And I press the "Search" button
    Then I should see "10_dollars_off" in the "name" field
    And I should see "2022-06-01" in the "start_at" field
    When I change "10_dollars_off" to "20_percent_off"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "20_percent_off" in the "name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "20_percent_off" in the results
    Then I should not see "10_dollars_off" in the results

# Scenario: Update a Pet
#     When I visit the "Home Page"
#     And I set the "Name" to "fido"
#     And I press the "Search" button
#     Then I should see "fido" in the "Name" field
#     And I should see "dog" in the "Category" field
#     When I change "Name" to "Boxer"
#     And I press the "Update" button
#     Then I should see the message "Success"
#     When I copy the "Id" field
#     And I press the "Clear" button
#     And I paste the "Id" field
#     And I press the "Retrieve" button
#     Then I should see "Boxer" in the "Name" field
#     When I press the "Clear" button
#     And I press the "Search" button
#     Then I should see "Boxer" in the results
#     Then I should not see "fido" in the results
