from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

@given('the database is clean')
def step_impl(context):
    # Use API to clean the database
    token = context.config.get('api_key')
    headers = {'Authorization': f'Bearer {token}'}
    context.api.delete('/api/test/cleanup', headers=headers)

@given('there is an admin user in the system')
def step_impl(context):
    for row in context.table:
        user_data = {
            'username': row['username'],
            'password': row['password'],
            'email': row['email']
        }
        context.api.post('/api/users', json=user_data)

@when('I visit the login page')
def step_impl(context):
    context.browser.get('http://localhost:3000/login')

@when('I enter "{text}" as {field}')
def step_impl(context, text, field):
    input_field = context.browser.find_element(By.ID, field)
    input_field.clear()
    input_field.send_keys(text)

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    button = context.browser.find_element(
        By.XPATH, f"//button[contains(text(), '{button_text}')]"
    )
    button.click()

@then('I should be redirected to the selection page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.url_to_be('http://localhost:3000/select')
    )

@then('I should see "{text}" on the page')
def step_impl(context, text):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
    )

@then('the JWT token should be stored in localStorage')
def step_impl(context):
    token = context.browser.execute_script("return localStorage.getItem('token');")
    assert token is not None and len(token) > 0

@then('I should see an error message "{message}"')
def step_impl(context, message):
    error = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'MuiAlert-message'))
    )
    assert message in error.text

@then('I should remain on the login page')
def step_impl(context):
    assert context.browser.current_url.endswith('/login')

@then('no JWT token should be stored')
def step_impl(context):
    token = context.browser.execute_script("return localStorage.getItem('token');")
    assert token is None

@given('I am logged in as "{username}"')
def step_impl(context, username):
    # First visit login page
    context.browser.get('http://localhost:3000/login')
    
    # Enter credentials
    username_input = context.browser.find_element(By.ID, 'username')
    password_input = context.browser.find_element(By.ID, 'password')
    
    username_input.send_keys(username)
    password_input.send_keys('admin')  # Using default password
    
    # Click login
    login_button = context.browser.find_element(
        By.XPATH, "//button[contains(text(), 'Sign In')]"
    )
    login_button.click()
    
    # Wait for redirect
    WebDriverWait(context.browser, 10).until(
        EC.url_to_be('http://localhost:3000/select')
    )

@when('I click on the user menu')
def step_impl(context):
    menu_button = context.browser.find_element(By.CLASS_NAME, 'MuiIconButton-root')
    menu_button.click()

@when('I click "{menu_item}"')
def step_impl(context, menu_item):
    menu_item_element = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{menu_item}')]"))
    )
    menu_item_element.click()

@then('the JWT token should be removed from localStorage')
def step_impl(context):
    token = context.browser.execute_script("return localStorage.getItem('token');")
    assert token is None

@when('I try to visit the "{url}" page directly')
def step_impl(context, url):
    context.browser.get(f'http://localhost:3000{url}')

@when('I refresh the page')
def step_impl(context):
    context.browser.refresh()

@then('I should remain logged in')
def step_impl(context):
    token = context.browser.execute_script("return localStorage.getItem('token');")
    assert token is not None and len(token) > 0

@then('I should see the same page I was on')
def step_impl(context):
    # Get current URL before refresh
    current_url = context.browser.current_url
    context.browser.refresh()
    WebDriverWait(context.browser, 10).until(
        lambda driver: driver.current_url == current_url
    )
