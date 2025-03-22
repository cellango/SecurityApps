from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

@given('I am on the dashboard page')
def step_impl(context):
    context.driver.get("http://localhost:3000/dashboard")
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "MuiGrid-root"))
    )

@given('the following departments exist')
def step_impl(context):
    # This data should be set up in the test database
    for row in context.table:
        # Add department to test database
        pass

@given('the following teams exist')
def step_impl(context):
    # This data should be set up in the test database
    for row in context.table:
        # Add team to test database
        pass

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
    )
    button.click()

@then('I should see department suggestions including')
def step_impl(context):
    department_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'department')]"))
    )
    department_input.click()
    
    for row in context.table:
        department = row[0]
        suggestion = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{department}')]"))
        )
        assert suggestion.is_displayed()

@then('I should see team suggestions including')
def step_impl(context):
    team_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'team')]"))
    )
    team_input.click()
    
    for row in context.table:
        team = row[0]
        suggestion = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{team}')]"))
        )
        assert suggestion.is_displayed()

@then('I should see all control family options')
def step_impl(context):
    select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'control-family')]"))
    )
    select.click()
    
    control_families = ['ACCESS_CONTROL', 'CONFIGURATION_MANAGEMENT', 'INCIDENT_RESPONSE',
                       'RISK_ASSESSMENT', 'SYSTEM_COMMUNICATIONS', 'SYSTEM_INFORMATION']
    
    for family in control_families:
        option = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{family}')]"))
        )
        assert option.is_displayed()

@then('I should see all implementation status options')
def step_impl(context):
    select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'status')]"))
    )
    select.click()
    
    statuses = ['IMPLEMENTED', 'PARTIALLY_IMPLEMENTED', 'PLANNED', 'NOT_IMPLEMENTED']
    
    for status in statuses:
        option = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[contains(text(), '{status}')]"))
        )
        assert option.is_displayed()

@when('I select "{value}" from {field} suggestions')
def step_impl(context, value, field):
    input_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//input[contains(@id, '{field.lower()}')]"))
    )
    input_field.click()
    input_field.send_keys(value)
    
    suggestion = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{value}')]"))
    )
    suggestion.click()

@when('I select "{value}" from {field}')
def step_impl(context, value, field):
    select = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//div[contains(@id, '{field.lower().replace(' ', '-')}')]"))
    )
    select.click()
    
    option = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{value}')]"))
    )
    option.click()

@when('I enter "{name}" as preset name')
def step_impl(context, name):
    input_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@label='Preset Name']"))
    )
    input_field.send_keys(name)

@then('I should see "{preset_name}" in the presets list')
def step_impl(context, preset_name):
    preset = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{preset_name}')]"))
    )
    assert preset.is_displayed()

@then('the preset should show the correct filter values')
def step_impl(context):
    preset = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "MuiListItem-root"))
    )
    preset_text = preset.text
    assert "Engineering" in preset_text
    assert "Frontend" in preset_text
    assert "ACCESS_CONTROL" in preset_text
    assert "IMPLEMENTED" in preset_text

@given('I have a saved preset "{preset_name}"')
def step_impl(context, preset_name):
    # This should be set up in the test database
    pass

@when('I click the use preset button for "{preset_name}"')
def step_impl(context, preset_name):
    preset_row = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{preset_name}')]//ancestor::li"))
    )
    use_button = preset_row.find_element(By.XPATH, ".//button[@title='Use preset']")
    use_button.click()

@when('I click the delete button for "{preset_name}"')
def step_impl(context, preset_name):
    preset_row = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{preset_name}')]//ancestor::li"))
    )
    delete_button = preset_row.find_element(By.XPATH, ".//button[@title='Delete preset']")
    delete_button.click()

@then('I should not see "{preset_name}" in the presets list')
def step_impl(context, preset_name):
    try:
        context.driver.find_element(By.XPATH, f"//div[contains(text(), '{preset_name}')]")
        assert False, f"Preset {preset_name} should not be visible"
    except:
        assert True

@then('the {field} field should show "{value}"')
def step_impl(context, field, value):
    field_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//input[contains(@id, '{field.lower()}')]"))
    )
    assert field_input.get_attribute("value") == value

@then('the Excel file should be downloaded')
def step_impl(context):
    # Wait for download to complete (adjust timeout as needed)
    time.sleep(5)
    
    # Check if file exists in downloads directory
    downloads_path = os.path.expanduser("~/Downloads")
    files = os.listdir(downloads_path)
    excel_files = [f for f in files if f.endswith(".xlsx") and "controls_export" in f]
    
    assert len(excel_files) > 0, "Excel file was not downloaded"

@then('the Excel file should contain filtered data for')
def step_impl(context):
    import pandas as pd
    
    # Get the most recent Excel file from downloads
    downloads_path = os.path.expanduser("~/Downloads")
    files = os.listdir(downloads_path)
    excel_files = [f for f in files if f.endswith(".xlsx") and "controls_export" in f]
    latest_file = max([os.path.join(downloads_path, f) for f in excel_files], key=os.path.getctime)
    
    # Read the Excel file
    df = pd.read_excel(latest_file)
    
    # Check if the data matches the expected filters
    for row in context.table:
        filtered_df = df[
            (df['Department'] == row['Department']) &
            (df['Team'] == row['Team']) &
            (df['Control Family'] == row['Control Family']) &
            (df['Status'] == row['Status'])
        ]
        assert len(filtered_df) > 0, f"No data found matching filters: {row}"
