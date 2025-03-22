from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am logged in as a security analyst')
def step_impl(context):
    context.driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=webdriver.ChromeOptions()
    )
    context.driver.get("http://appinventory_frontend:3000")
    # Add login steps here

@when('I create a new application with the following details')
def step_impl(context):
    context.driver.find_element(By.ID, "create-app-button").click()
    for row in context.table:
        context.driver.find_element(By.ID, "name").send_keys(row['name'])
        context.driver.find_element(By.ID, "description").send_keys(row['description'])
        context.driver.find_element(By.ID, "application-type").send_keys(row['application_type'])
        context.driver.find_element(By.ID, "state").send_keys(row['state'])
        context.driver.find_element(By.ID, "owner-id").send_keys(row['owner_id'])
    context.driver.find_element(By.ID, "submit-button").click()

@then('the application should be created successfully')
def step_impl(context):
    success_message = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()

@then('I should see the application in the list')
def step_impl(context):
    app_list = context.driver.find_elements(By.CLASS_NAME, "application-item")
    assert len(app_list) > 0

@given('there is an existing application "{app_name}"')
def step_impl(context, app_name):
    context.app_name = app_name
    # Add setup code to ensure application exists

@when('I update the application state to "{new_state}"')
def step_impl(context, new_state):
    app_element = context.driver.find_element(By.XPATH, f"//div[contains(text(), '{context.app_name}')]")
    app_element.find_element(By.CLASS_NAME, "edit-button").click()
    state_input = context.driver.find_element(By.ID, "state")
    state_input.clear()
    state_input.send_keys(new_state)
    context.driver.find_element(By.ID, "save-button").click()

@then('the application state should be updated')
def step_impl(context):
    success_message = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()

@then('an audit log should be created for the change')
def step_impl(context):
    context.driver.get("http://appinventory_frontend:3000/audit-logs")
    audit_logs = WebDriverWait(context.driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "audit-log-item"))
    )
    assert len(audit_logs) > 0

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
