from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@given('I am logged in as a security analyst')
def step_impl(context):
    # Navigate to login page
    context.driver.get(f"{context.base_url}/login")
    
    # Find and fill login form
    username_input = context.driver.find_element(By.ID, "username")
    password_input = context.driver.find_element(By.ID, "password")
    
    username_input.send_keys("test_analyst")
    password_input.send_keys("test_password")
    
    # Submit login form
    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Wait for dashboard to load
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )

@given('I am on the application details page for application "{app_name}"')
def step_impl(context, app_name):
    # Navigate to application details page
    context.driver.get(f"{context.base_url}/applications/{app_name}")
    
    # Wait for page to load
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "application-details"))
    )

@then('I should see the security score displayed')
def step_impl(context):
    score_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "security-score"))
    )
    assert score_element.is_displayed()

@then('the score should be between {min_score:d} and {max_score:d}')
def step_impl(context, min_score, max_score):
    score_element = context.driver.find_element(By.CLASS_NAME, "security-score")
    score = int(float(score_element.text))
    assert min_score <= score <= max_score

@then('I should see the last scored date')
def step_impl(context):
    date_element = context.driver.find_element(By.CLASS_NAME, "last-scored-date")
    assert date_element.is_displayed()

@when('I click on the "{tab_name}" tab')
def step_impl(context, tab_name):
    tab = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{tab_name}')]"))
    )
    tab.click()

@then('I should see a list of security findings')
def step_impl(context):
    findings_list = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "findings-list"))
    )
    findings = findings_list.find_elements(By.CLASS_NAME, "finding-item")
    assert len(findings) > 0

@then('each finding should display severity level')
def step_impl(context):
    findings = context.driver.find_elements(By.CLASS_NAME, "finding-item")
    for finding in findings:
        severity = finding.find_element(By.CLASS_NAME, "severity")
        assert severity.is_displayed()

@then('each finding should display discovery date')
def step_impl(context):
    findings = context.driver.find_elements(By.CLASS_NAME, "finding-item")
    for finding in findings:
        date = finding.find_element(By.CLASS_NAME, "discovery-date")
        assert date.is_displayed()

@when('I select severity "{severity}" from the filter')
def step_impl(context, severity):
    # Open severity filter dropdown
    filter_button = context.driver.find_element(By.CLASS_NAME, "severity-filter")
    filter_button.click()
    
    # Select severity option
    severity_option = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{severity}')]"))
    )
    severity_option.click()

@then('I should only see findings with "{severity}" severity')
def step_impl(context, severity):
    # Wait for findings to be filtered
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "findings-list"))
    )
    
    findings = context.driver.find_elements(By.CLASS_NAME, "finding-item")
    for finding in findings:
        severity_element = finding.find_element(By.CLASS_NAME, "severity")
        assert severity_element.text == severity
