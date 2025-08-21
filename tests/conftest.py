"""
Pytest configuration and fixtures
"""
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from main import app
from src.database import get_db
from src.models import Base
from config.settings import settings

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database"""
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    
    # Remove test database file
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def test_headers():
    """Test API headers"""
    return {"X-API-Key": settings.api_key}

@pytest.fixture
def mock_fmcsa_success():
    """Mock successful FMCSA API response"""
    return {
        "content": [{
            "legalName": "Test Trucking LLC",
            "dbaName": "Test Express",
            "entityType": "CARRIER",
            "operatingStatus": "ACTIVE",
            "outOfServiceDate": None,
            "mcs150Date": "2023-01-15",
            "mcs150Mileage": 50000,
            "phyStreet": "123 Test St",
            "phyCity": "Test City",
            "phyState": "TX",
            "phyZipcode": "12345",
            "phyPhone": "(555) 123-4567"
        }]
    }

@pytest.fixture
def sample_load_data():
    """Sample load data for testing"""
    return {
        "load_id": "TEST001",
        "origin": "Chicago, IL",
        "destination": "Atlanta, GA",
        "pickup_datetime": "2024-01-20T08:00:00Z",
        "delivery_datetime": "2024-01-21T17:00:00Z",
        "equipment_type": "Dry Van",
        "loadboard_rate": 2500.00,
        "notes": "Test load",
        "weight": 42000,
        "commodity_type": "Electronics",
        "num_of_pieces": 25,
        "miles": 588,
        "dimensions": "53' x 8.5' x 9'"
    }
