"""Test Configuration and Fixtures"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def sample_workflow_data():
    """Sample workflow data for testing"""
    return {
        "name": "Test Workflow",
        "description": "A test workflow",
        "trigger": {
            "type": "manual",
            "config": {}
        },
        "steps": []
    }
