from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am logged in as a security assessor')
def step_impl(context):
    context.driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=webdriver.ChromeOptions()
    )
    context.driver.get("http://appscore_frontend:3000")
    # Add login steps here

@when('I create a new security assessment for application "{app_name}" with the following scores')
def step_impl(context, app_name):
    context.driver.find_element(By.ID, "new-assessment-button").click()
    context.driver.find_element(By.ID, "application-select").send_keys(app_name)
    
    for row in context.table:
        category = row['category']
        metric = row['metric']
        score = row['score']
        
        category_elem = context.driver.find_element(By.XPATH, f"//div[contains(text(), '{category}')]")
        category_elem.find_element(By.XPATH, f".//input[@name='{metric}']").send_keys(score)
    
    context.driver.find_element(By.ID, "submit-assessment").click()

@then('the security score should be calculated correctly')
def step_impl(context):
    total_score = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "total-score"))
    )
    assert float(total_score.text) > 0

@then('the assessment should be saved successfully')
def step_impl(context):
    success_message = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert success_message.is_displayed()

@given('there is an application with multiple security assessments')
def step_impl(context):
    # Setup code to ensure application has multiple assessments
    pass

@when('I view the security score history')
def step_impl(context):
    context.driver.find_element(By.ID, "view-history-button").click()

@then('I should see a list of all assessments')
def step_impl(context):
    assessments = WebDriverWait(context.driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "assessment-item"))
    )
    assert len(assessments) > 0

@then('the scores should be displayed in chronological order')
def step_impl(context):
    dates = context.driver.find_elements(By.CLASS_NAME, "assessment-date")
    date_list = [date.text for date in dates]
    assert date_list == sorted(date_list, reverse=True)

def after_scenario(context, scenario):
    if hasattr(context, 'driver'):
        context.driver.quit()
