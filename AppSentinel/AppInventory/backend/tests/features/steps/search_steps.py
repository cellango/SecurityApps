from behave import given, when, then
from flask import session
from app.models import Application, User
from app import db

@given('I am logged in as a user')
def step_impl(context):
    user = User(username='testuser', password='testpass')
    db.session.add(user)
    db.session.commit()
    with context.client.session_transaction() as sess:
        sess['user_id'] = user.id
        sess['token'] = 'valid_token'

@given('the following applications exist')
def step_impl(context):
    for row in context.table:
        app = Application(
            name=row['name'],
            description=row['description'],
            department_name=row['department_name'],
            team_name=row['team_name']
        )
        db.session.add(app)
    db.session.commit()

@when('I type "{query}" in the search box')
def step_impl(context, query):
    context.response = context.client.get(f'/api/applications/search?q={query}',
                                        headers={'Authorization': 'Bearer valid_token'})

@then('I should see "{app_name}" in the search results')
def step_impl(context, app_name):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert any(app['name'] == app_name for app in data)

@then('I should not see "{app_name}" in the search results')
def step_impl(context, app_name):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert not any(app['name'] == app_name for app in data)

@then('the result should show "{department}" as the department')
def step_impl(context, department):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert any(app['department_name'] == department for app in data)

@then('I should see "{message}" message')
def step_impl(context, message):
    assert context.response.status_code in [200, 401]
    if context.response.status_code == 401:
        assert message in context.response.get_json()['message']
    else:
        data = context.response.get_json()
        assert len(data) == 0 or message in str(data)

@given('I am not logged in')
def step_impl(context):
    with context.client.session_transaction() as sess:
        sess.clear()

@given('my session has expired')
def step_impl(context):
    with context.client.session_transaction() as sess:
        sess.clear()
    context.response = context.client.get('/api/applications/search?q=test',
                                        headers={'Authorization': 'Bearer expired_token'})
