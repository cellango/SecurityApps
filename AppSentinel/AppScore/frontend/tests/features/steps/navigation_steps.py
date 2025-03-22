from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('the following teams exist')
def step_impl(context):
    for row in context.table:
        team_data = {
            'name': row['name'],
            'description': row['description']
        }
        context.api.post('/api/teams', json=team_data)

@given('the following applications exist')
def step_impl(context):
    for row in context.table:
        app_data = {
            'name': row['name'],
            'team': row['team'],
            'security_score': int(row['security_score'])
        }
        context.api.post('/api/applications', json=app_data)

@when('I log in successfully')
def step_impl(context):
    context.execute_steps('''
        When I visit the login page
        And I enter "admin" as username
        And I enter "admin" as password
        And I click the "Sign In" button
    ''')

@then('I should see the selection page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'selection-page'))
    )

@then('I should see two options')
def step_impl(context):
    for row in context.table:
        option = row['option']
        WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//button[contains(text(), '{option}')]"))
        )

@given('I am on the selection page')
def step_impl(context):
    context.browser.get('http://localhost:3000/select')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'selection-page'))
    )

@when('I click "{button_text}"')
def step_impl(context, button_text):
    button = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
    )
    button.click()

@then('I should see the teams list')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'teams-list'))
    )

@then('I should see the following teams')
def step_impl(context):
    for row in context.table:
        team_row = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(., '{row['name']}')]"))
        )
        assert row['app_count'] in team_row.text
        assert row['avg_score'] in team_row.text

@given('I am on the teams list')
def step_impl(context):
    context.browser.get('http://localhost:3000/teams')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'teams-list'))
    )

@when('I click on "{team_name}"')
def step_impl(context, team_name):
    team_element = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//tr[contains(., '{team_name}')]"))
    )
    team_element.click()

@then('I should see the team\'s applications page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'team-applications'))
    )

@then('I should see "{app_name}" in the applications list')
def step_impl(context, app_name):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//tr[contains(., '{app_name}')]"))
    )

@then('I should not see "{app_name}" in the applications list')
def step_impl(context, app_name):
    WebDriverWait(context.browser, 10).until_not(
        EC.presence_of_element_located((By.XPATH, f"//tr[contains(., '{app_name}')]"))
    )

@then('I should see all applications')
def step_impl(context):
    for row in context.table:
        app_row = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//tr[contains(., '{row['name']}')]"))
        )
        assert row['team'] in app_row.text
        assert row['score'] in app_row.text

@given('I am on the applications list')
def step_impl(context):
    context.browser.get('http://localhost:3000/applications')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'applications-list'))
    )

@when('I click on application "{app_name}"')
def step_impl(context, app_name):
    app_element = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//tr[contains(., '{app_name}')]"))
    )
    app_element.click()

@then('I should see the application details page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'application-details'))
    )

@then('I should see the security score breakdown')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'score-breakdown'))
    )

@then('I should see the remediation recommendations')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'remediation-list'))
    )

@given('I am on the application details page')
def step_impl(context):
    context.browser.get('http://localhost:3000/applications/1')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'application-details'))
    )

@when('I click the back button')
def step_impl(context):
    back_button = context.browser.find_element(By.CLASS_NAME, 'back-button')
    back_button.click()

@then('I should return to the applications list')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'applications-list'))
    )

@then('I should return to the selection page')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'selection-page'))
    )

@given('I am viewing "{app_name}" details from the team view')
def step_impl(context, app_name):
    context.browser.get(f'http://localhost:3000/teams/1/applications/{app_name}')
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'application-details'))
    )

@then('I should see the breadcrumb trail')
def step_impl(context):
    breadcrumbs = context.browser.find_element(By.CLASS_NAME, 'breadcrumbs')
    for row in context.table:
        level = int(row['level'])
        text = row['text']
        breadcrumb = breadcrumbs.find_element(
            By.XPATH, f".//li[{level}][contains(text(), '{text}')]"
        )
        assert breadcrumb is not None
