from behave import given, when, then
from flask import session
from app.models import User
from app import db

@given('I am on the login page')
def step_impl(context):
    context.response = context.client.get('/login')
    assert context.response.status_code == 200

@when('I enter valid credentials')
def step_impl(context):
    credentials = context.table[0]
    user = User(username=credentials['username'])
    user.set_password(credentials['password'])
    db.session.add(user)
    db.session.commit()
    
    context.response = context.client.post('/login', json={
        'username': credentials['username'],
        'password': credentials['password']
    })

@when('I enter invalid credentials')
def step_impl(context):
    credentials = context.table[0]
    context.response = context.client.post('/login', json={
        'username': credentials['username'],
        'password': credentials['password']
    })

@then('I should be redirected to the dashboard')
def step_impl(context):
    assert context.response.status_code == 302
    assert context.response.location.endswith('/dashboard')

@then('I should see my username in the navigation bar')
def step_impl(context):
    with context.client.session_transaction() as sess:
        assert 'user_id' in sess
        assert 'token' in sess

@then('I should see an error message "{message}"')
def step_impl(context, message):
    assert context.response.status_code == 401
    assert message in context.response.get_json()['message']

@then('I should remain on the login page')
def step_impl(context):
    assert context.response.status_code == 401

@when('I click the logout button')
def step_impl(context):
    context.response = context.client.post('/logout')

@then('I should not be able to access protected resources')
def step_impl(context):
    response = context.client.get('/api/applications')
    assert response.status_code == 401

@when('my session expires')
def step_impl(context):
    with context.client.session_transaction() as sess:
        sess.clear()

@when('I try to access a protected resource')
def step_impl(context):
    context.response = context.client.get('/api/applications')
