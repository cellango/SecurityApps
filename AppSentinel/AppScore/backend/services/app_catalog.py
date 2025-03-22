import os
import aiohttp
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.application import Application, Base

class AppCatalogService:
    def __init__(self):
        self.api_url = os.getenv('APP_CATALOG_API_URL')
        self.api_key = os.getenv('APP_CATALOG_API_KEY')
        self.cache_ttl = timedelta(hours=1)  # Cache TTL of 1 hour
        
        # Initialize database
        self.engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///app.db'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    async def get_application(self, catalog_id: str) -> Optional[Application]:
        """Get application from cache or API"""
        session = self.Session()
        try:
            app = session.query(Application).filter_by(catalog_id=catalog_id).first()
            
            # If app exists and cache is fresh, return it
            if app and app.last_synced and datetime.utcnow() - app.last_synced < self.cache_ttl:
                return app

            # Otherwise, fetch from API
            app_data = await self._fetch_from_api(catalog_id)
            if not app_data:
                return None

            if app:
                # Update existing app
                app.name = app_data['name']
                app.description = app_data.get('description')
                app.metadata = app_data.get('metadata', {})
                app.last_synced = datetime.utcnow()
            else:
                # Create new app
                app = Application(
                    catalog_id=catalog_id,
                    name=app_data['name'],
                    description=app_data.get('description'),
                    metadata=app_data.get('metadata', {}),
                    last_synced=datetime.utcnow()
                )
                session.add(app)

            session.commit()
            return app

        finally:
            session.close()

    async def sync_all_applications(self):
        """Sync all applications from the catalog"""
        session = self.Session()
        try:
            # Fetch all applications from API
            async with aiohttp.ClientSession() as http_session:
                async with http_session.get(
                    f'{self.api_url}/applications',
                    headers={'Authorization': f'Bearer {self.api_key}'}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch applications: {response.status}")
                    
                    apps_data = await response.json()

            # Update or create applications
            for app_data in apps_data:
                app = session.query(Application).filter_by(catalog_id=app_data['id']).first()
                
                if app:
                    app.name = app_data['name']
                    app.description = app_data.get('description')
                    app.metadata = app_data.get('metadata', {})
                    app.last_synced = datetime.utcnow()
                else:
                    app = Application(
                        catalog_id=app_data['id'],
                        name=app_data['name'],
                        description=app_data.get('description'),
                        metadata=app_data.get('metadata', {}),
                        last_synced=datetime.utcnow()
                    )
                    session.add(app)

            session.commit()

        finally:
            session.close()

    async def _fetch_from_api(self, catalog_id: str) -> Optional[dict]:
        """Fetch application data from API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.api_url}/applications/{catalog_id}',
                    headers={'Authorization': f'Bearer {self.api_key}'}
                ) as response:
                    if response.status != 200:
                        return None
                    return await response.json()
        except Exception as e:
            print(f"Error fetching from API: {str(e)}")
            return None

    def add_test_data(self):
        """Add test applications to the database"""
        session = self.Session()
        try:
            # Clear existing test data
            session.query(Application).delete()
            
            # Add test applications
            test_apps = [
                Application(
                    catalog_id='1',
                    name='App1',
                    description='Test Application 1',
                    metadata={'type': 'internal'},
                    last_synced=datetime.utcnow()
                ),
                Application(
                    catalog_id='2',
                    name='App2',
                    description='Test Application 2',
                    metadata={'type': 'external'},
                    last_synced=datetime.utcnow()
                )
            ]
            
            for app in test_apps:
                session.add(app)
            
            session.commit()
            
        finally:
            session.close()
