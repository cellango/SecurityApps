from behave import given, when, then
from app.models import User, AuditLog
from app import db

@given('I am logged in as an administrator')
def step_impl(context):
    admin = User(username='admin', role='ADMIN')
    admin.set_password('adminpass')
    db.session.add(admin)
    db.session.commit()
    
    context.response = context.client.post('/login', json={
        'username': 'admin',
        'password': 'adminpass'
    })
    assert context.response.status_code == 200

@given('the following users exist')
def step_impl(context):
    for row in context.table:
        user = User(
            username=row['username'],
            role=row['role'],
            department=row['department']
        )
        user.set_password('password123')
        db.session.add(user)
    db.session.commit()

@when('I navigate to user management')
def step_impl(context):
    context.response = context.client.get('/admin/users')
    assert context.response.status_code == 200

@when('I create a new user with details')
def step_impl(context):
    user_data = context.table[0]
    context.response = context.client.post('/admin/users', json={
        'username': user_data['username'],
        'password': user_data['password'],
        'role': user_data['role'],
        'department': user_data['department']
    })

@then('the user should be created successfully')
def step_impl(context):
    assert context.response.status_code == 201
    user = User.query.filter_by(username=context.table[0]['username']).first()
    assert user is not None

@when('I select user "{username}"')
def step_impl(context, username):
    context.selected_user = User.query.filter_by(username=username).first()
    assert context.selected_user is not None

@when('I change their role to "{role}"')
def step_impl(context, role):
    context.response = context.client.put(f'/admin/users/{context.selected_user.id}', json={
        'role': role
    })

@then('the user\'s role should be updated')
def step_impl(context):
    assert context.response.status_code == 200
    user = User.query.get(context.selected_user.id)
    assert user.role == 'ADMIN'

@when('I disable their account')
def step_impl(context):
    context.response = context.client.put(f'/admin/users/{context.selected_user.id}', json={
        'is_active': False
    })

@then('the user\'s account should be disabled')
def step_impl(context):
    assert context.response.status_code == 200
    user = User.query.get(context.selected_user.id)
    assert not user.is_active

@then('an audit log should be created for the {action}')
def step_impl(context, action):
    log = AuditLog.query.filter_by(action=action).first()
    assert log is not None

@when('I filter by department "{department}"')
def step_impl(context, department):
    context.response = context.client.get(f'/admin/users?department={department}')

@when('I search for "{query}"')
def step_impl(context, query):
    context.response = context.client.get(f'/admin/users?search={query}')
