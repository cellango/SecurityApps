from behave import given, when, then
from app.models import Application
from app import db

@when('I visit the dashboard page')
def step_impl(context):
    context.response = context.client.get('/dashboard')
    assert context.response.status_code == 200

@then('I should see the total number of applications')
def step_impl(context):
    data = context.response.get_json()
    assert 'total_applications' in data
    assert data['total_applications'] == Application.query.count()

@then('I should see applications by state')
def step_impl(context):
    data = context.response.get_json()
    assert 'applications_by_state' in data
    for row in context.table:
        state = row['state']
        count = int(row['count'])
        assert data['applications_by_state'][state] == count

@then('I should see applications by type')
def step_impl(context):
    data = context.response.get_json()
    assert 'applications_by_type' in data
    for row in context.table:
        app_type = row['type']
        count = int(row['count'])
        assert data['applications_by_type'][app_type] == count

@when('I select department "{department}"')
def step_impl(context, department):
    context.response = context.client.get(f'/dashboard?department={department}')

@then('I should see {count:d} application(s)')
def step_impl(context, count):
    data = context.response.get_json()
    assert len(data['applications']) == count

@then('I should see "{app_name}"')
def step_impl(context, app_name):
    data = context.response.get_json()
    assert any(app['name'] == app_name for app in data['applications'])

@then('I should not see "{app_name}"')
def step_impl(context, app_name):
    data = context.response.get_json()
    assert not any(app['name'] == app_name for app in data['applications'])

@when('I click the "{column}" column header')
def step_impl(context, column):
    context.response = context.client.get(f'/dashboard?sort={column.lower()}')

@then('the applications should be sorted alphabetically')
def step_impl(context):
    data = context.response.get_json()
    names = [app['name'] for app in data['applications']]
    assert names == sorted(names)

@when('I click the "Export" button')
def step_impl(context):
    context.export_format = None

@when('I select format "{format}"')
def step_impl(context, format):
    context.export_format = format.lower()
    context.response = context.client.get(f'/dashboard/export?format={context.export_format}')

@then('a CSV file should be downloaded')
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'text/csv'
    assert 'attachment' in context.response.headers['Content-Disposition']
