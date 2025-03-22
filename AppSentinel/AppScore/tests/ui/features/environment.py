from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def before_all(context):
    # Set base URL for the application
    context.base_url = "http://localhost:3000"

def before_scenario(context, scenario):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.implicitly_wait(10)
    
def after_scenario(context, scenario):
    # Clean up WebDriver
    if hasattr(context, 'driver'):
        context.driver.quit()

def after_step(context, step):
    # Take screenshot if step fails
    if step.status == "failed":
        context.driver.save_screenshot(f"failed_step_{step.name}.png")
