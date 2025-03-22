from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import json

def before_all(context):
    # Set up Chrome options
    chrome_options = Options()
    if os.getenv('HEADLESS', 'false').lower() == 'true':
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Initialize WebDriver
    context.browser = webdriver.Chrome(options=chrome_options)
    context.browser.implicitly_wait(10)
    
    # Load test configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path) as f:
        context.config = json.load(f)

def after_all(context):
    # Clean up WebDriver
    context.browser.quit()

def before_scenario(context, scenario):
    # Reset application state before each scenario
    context.browser.delete_all_cookies()
    
    # Set up test data if needed
    if 'requires_test_data' in scenario.tags:
        setup_test_data(context)

def after_scenario(context, scenario):
    # Clean up test data if needed
    if 'requires_test_data' in scenario.tags:
        cleanup_test_data(context)

def setup_test_data(context):
    """Set up test data for scenarios"""
    # Add test applications via API
    test_apps = [
        {
            'name': 'App1',
            'description': 'Test Application 1',
            'team': 'Security Team'
        },
        {
            'name': 'App2',
            'description': 'Test Application 2',
            'team': 'Development Team'
        }
    ]
    
    # Use API to create test data
    api_url = context.config['api_url']
    headers = {'Authorization': f'Bearer {context.config["api_key"]}'}
    
    for app in test_apps:
        requests.post(f'{api_url}/applications', json=app, headers=headers)

def cleanup_test_data(context):
    """Clean up test data after scenarios"""
    # Remove test applications via API
    api_url = context.config['api_url']
    headers = {'Authorization': f'Bearer {context.config["api_key"]}'}
    
    test_apps = ['App1', 'App2']
    for app_name in test_apps:
        requests.delete(f'{api_url}/applications/{app_name}', headers=headers)
