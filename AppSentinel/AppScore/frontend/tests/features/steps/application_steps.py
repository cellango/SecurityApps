from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

@given('I am logged in as a security engineer')
def step_impl(context):
    context.browser.get('http://localhost:3000/login')
    username_input = context.browser.find_element(By.ID, 'username')
    password_input = context.browser.find_element(By.ID, 'password')
    
    username_input.send_keys('test_engineer')
    password_input.send_keys('test_password')
    password_input.send_keys(Keys.RETURN)
    
    # Wait for redirect to complete
    WebDriverWait(context.browser, 10).until(
        EC.url_to_be('http://localhost:3000/applications')
    )

@given('there are test applications in the system')
def step_impl(context):
    # This step assumes test data is already loaded
    # You might want to use API calls to ensure test data exists
    for row in context.table:
        # Verify test data exists or create it
        pass

@when('I visit the application list page')
def step_impl(context):
    context.browser.get('http://localhost:3000/applications')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'application-list'))
    )

@then('I should see the following applications')
def step_impl(context):
    app_list = context.browser.find_elements(By.CLASS_NAME, 'application-row')
    
    # Create a list of actual application names
    actual_apps = []
    for app in app_list:
        name = app.find_element(By.CLASS_NAME, 'app-name').text
        description = app.find_element(By.CLASS_NAME, 'app-description').text
        actual_apps.append({'name': name, 'description': description})
    
    # Compare with expected applications
    expected_apps = [{'name': row['name'], 'description': row['description']} 
                    for row in context.table]
    
    assert len(actual_apps) == len(expected_apps), \
        f"Expected {len(expected_apps)} applications, but found {len(actual_apps)}"
    
    for expected in expected_apps:
        assert expected in actual_apps, \
            f"Application {expected['name']} not found in the list"

@then('each application should display its current security score')
def step_impl(context):
    score_elements = context.browser.find_elements(By.CLASS_NAME, 'security-score')
    
    for score in score_elements:
        score_value = float(score.text.strip('%'))
        assert 0 <= score_value <= 100, \
            f"Invalid score value: {score_value}"

@when('I click on application "{app_name}"')
def step_impl(context, app_name):
    app_element = context.browser.find_element(
        By.XPATH, f"//div[contains(@class, 'application-row') and .//text()='{app_name}']"
    )
    app_element.click()
    
    # Wait for details page to load
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'application-details'))
    )

@then('I should see the application details page')
def step_impl(context):
    assert context.browser.find_element(By.CLASS_NAME, 'application-details')

@then('I should see the security score breakdown')
def step_impl(context):
    for row in context.table:
        score_type = row['score_type']
        expected_value = float(row['value'])
        
        score_element = context.browser.find_element(
            By.XPATH, f"//div[contains(@class, 'score-breakdown')]//div[contains(text(), '{score_type}')]"
        )
        actual_value = float(score_element.find_element(By.CLASS_NAME, 'score-value').text)
        
        assert abs(actual_value - expected_value) < 0.1, \
            f"Expected {score_type} to be {expected_value}, but got {actual_value}"

@when('I select team "{team_name}"')
def step_impl(context, team_name):
    team_dropdown = context.browser.find_element(By.ID, 'team-select')
    team_dropdown.click()
    
    team_option = context.browser.find_element(
        By.XPATH, f"//li[contains(text(), '{team_name}')]"
    )
    team_option.click()

@then('I should only see applications for "{team_name}"')
def step_impl(context, team_name):
    # Wait for filter to apply
    time.sleep(1)
    
    app_list = context.browser.find_elements(By.CLASS_NAME, 'application-row')
    for app in app_list:
        team_element = app.find_element(By.CLASS_NAME, 'app-team')
        assert team_element.text == team_name, \
            f"Found application for team {team_element.text}, expected {team_name}"

@when('I click on "{button_text}"')
def step_impl(context, button_text):
    button = context.browser.find_element(
        By.XPATH, f"//*[contains(text(), '{button_text}')]"
    )
    button.click()

@then('I should see a chart of historical scores')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'score-history-chart'))
    )

@then('I should see at least {count:d} historical data points')
def step_impl(context, count):
    data_points = context.browser.find_elements(By.CLASS_NAME, 'chart-data-point')
    assert len(data_points) >= count, \
        f"Expected at least {count} data points, but found {len(data_points)}"

@then('I should see a list of remediation items')
def step_impl(context):
    remediation_list = context.browser.find_element(By.CLASS_NAME, 'remediation-list')
    items = remediation_list.find_elements(By.CLASS_NAME, 'remediation-item')
    assert len(items) > 0, "No remediation items found"

@then('each remediation should have')
def step_impl(context):
    remediation_items = context.browser.find_elements(By.CLASS_NAME, 'remediation-item')
    
    for item in remediation_items:
        for row in context.table:
            field = row['field'].lower()
            assert item.find_element(By.CLASS_NAME, f'remediation-{field}'), \
                f"Remediation item missing field: {field}"

@when('I enter "{search_text}" in the search box')
def step_impl(context, search_text):
    search_box = context.browser.find_element(By.ID, 'application-search')
    search_box.clear()
    search_box.send_keys(search_text)
    time.sleep(1)  # Wait for search to apply

@then('I should see applications containing "{text}"')
def step_impl(context, text):
    app_list = context.browser.find_elements(By.CLASS_NAME, 'application-row')
    assert len(app_list) > 0, "No applications found"
    
    for app in app_list:
        app_name = app.find_element(By.CLASS_NAME, 'app-name').text
        assert text.lower() in app_name.lower(), \
            f"Application {app_name} does not contain search text {text}"

@then('I should not see unmatched applications')
def step_impl(context):
    app_list = context.browser.find_elements(By.CLASS_NAME, 'application-row')
    for app in app_list:
        app_name = app.find_element(By.CLASS_NAME, 'app-name').text
        assert "App" in app_name, \
            f"Found unmatched application: {app_name}"
