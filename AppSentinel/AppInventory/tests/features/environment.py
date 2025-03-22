from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app, db
from app.models import Application, SecurityControl, ExportFilterPreset
import os
import threading
import time
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def before_all(context):
    # Set up Flask app in testing mode
    context.app = create_app('testing')
    context.app_server = ServerThread(context.app)
    context.app_server.start()
    time.sleep(1)  # Give the server a second to start

    # Set up Chrome WebDriver
    chrome_options = Options()
    if os.environ.get('CI'):  # If running in CI environment
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    context.driver.implicitly_wait(10)

def before_scenario(context, scenario):
    # Clear database
    with context.app.app_context():
        db.drop_all()
        db.create_all()
        
        # Add test data
        departments = ['Engineering', 'IT Security', 'Compliance']
        teams = ['Frontend', 'Backend', 'DevOps']
        
        for dept in departments:
            for team in teams:
                app = Application(
                    name=f"{dept} {team} App",
                    department_name=dept,
                    team_name=team
                )
                db.session.add(app)
        
        db.session.commit()

def after_scenario(context, scenario):
    # Clean up any downloads
    downloads_path = os.path.expanduser("~/Downloads")
    for file in os.listdir(downloads_path):
        if file.endswith(".xlsx") and "controls_export" in file:
            os.remove(os.path.join(downloads_path, file))

def after_all(context):
    # Clean up
    context.driver.quit()
    context.app_server.shutdown()
    context.app_server.join()
