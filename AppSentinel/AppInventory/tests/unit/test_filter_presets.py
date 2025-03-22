import unittest
from datetime import datetime, date
from app import create_app, db
from app.models import ExportFilterPreset, ControlFamily, ControlStatus
import json

class TestFilterPresets(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test preset
        self.test_preset = ExportFilterPreset(
            name="Test Preset",
            department="Engineering",
            team="Frontend",
            control_family=ControlFamily.ACCESS_CONTROL,
            status=ControlStatus.IMPLEMENTED,
            implementation_date_start=date(2024, 1, 1),
            implementation_date_end=date(2024, 12, 31)
        )
        db.session.add(self.test_preset)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_preset(self):
        """Test creating a new filter preset"""
        data = {
            "name": "New Preset",
            "department": "IT Security",
            "team": "Backend",
            "control_family": "INCIDENT_RESPONSE",
            "status": "PLANNED",
            "implementation_date_start": "2024-01-01",
            "implementation_date_end": "2024-12-31"
        }
        
        response = self.client.post(
            '/api/dashboard/filters/presets',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        preset = ExportFilterPreset.query.filter_by(name="New Preset").first()
        self.assertIsNotNone(preset)
        self.assertEqual(preset.department, "IT Security")
        self.assertEqual(preset.control_family, ControlFamily.INCIDENT_RESPONSE)

    def test_get_presets(self):
        """Test retrieving all filter presets"""
        response = self.client.get('/api/dashboard/filters/presets')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Preset")
        self.assertEqual(data[0]['department'], "Engineering")

    def test_delete_preset(self):
        """Test deleting a filter preset"""
        response = self.client.delete(f'/api/dashboard/filters/presets/{self.test_preset.id}')
        self.assertEqual(response.status_code, 204)
        
        preset = ExportFilterPreset.query.get(self.test_preset.id)
        self.assertIsNone(preset)

    def test_use_preset(self):
        """Test marking a preset as used"""
        response = self.client.post(f'/api/dashboard/filters/presets/{self.test_preset.id}/use')
        self.assertEqual(response.status_code, 200)
        
        preset = ExportFilterPreset.query.get(self.test_preset.id)
        self.assertIsNotNone(preset.last_used)

    def test_get_filter_suggestions(self):
        """Test getting filter suggestions"""
        response = self.client.get('/api/dashboard/filters/suggestions')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('departments', data)
        self.assertIn('teams', data)
        self.assertIn('control_families', data)
        self.assertIn('statuses', data)
        self.assertIn('implementation_date_range', data)

    def test_invalid_preset_name(self):
        """Test creating a preset without a name"""
        data = {
            "department": "IT Security",
            "team": "Backend"
        }
        
        response = self.client.post(
            '/api/dashboard/filters/presets',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_invalid_preset_id(self):
        """Test operations with non-existent preset ID"""
        response = self.client.delete('/api/dashboard/filters/presets/999')
        self.assertEqual(response.status_code, 404)
        
        response = self.client.post('/api/dashboard/filters/presets/999/use')
        self.assertEqual(response.status_code, 404)

    def test_duplicate_preset_name(self):
        """Test creating a preset with duplicate name"""
        data = {
            "name": "Test Preset",  # Same name as existing preset
            "department": "IT Security"
        }
        
        response = self.client.post(
            '/api/dashboard/filters/presets',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
