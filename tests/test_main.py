"""
Test suite for the Inbound Sales AI Agent
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests

from main import app
from src.database import get_db
from src.models import Base
from src.schemas import LoadCreate, CallStart, FMCSACarrierInfo
from config.settings import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Test headers
TEST_HEADERS = {"X-API-Key": settings.api_key}


class TestLoadManagement:
    """Test load management endpoints"""
    
    def test_create_load(self):
        """Test creating a new load"""
        import time
        unique_id = f"TEST{int(time.time() * 1000)}"  # Unique ID based on timestamp
        load_data = {
            "load_id": unique_id,
            "origin": "Test Origin",
            "destination": "Test Destination",
            "pickup_datetime": "2024-01-25T10:00:00Z",
            "delivery_datetime": "2024-01-26T18:00:00Z",
            "equipment_type": "Dry Van",
            "loadboard_rate": 2000.00,
            "notes": "Test load",
            "weight": 40000,
            "commodity_type": "Test Commodity",
            "num_of_pieces": 10,
            "miles": 500,
            "dimensions": "53' x 8.5' x 9'"
        }
        
        response = client.post("/api/loads", json=load_data, headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert data["load_id"] == unique_id
        assert data["origin"] == "Test Origin"
        assert data["status"] == "available"
    
    def test_get_loads(self):
        """Test retrieving loads"""
        response = client.get("/api/loads", headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_search_loads(self):
        """Test load search functionality"""
        response = client.get(
            "/api/loads/search?origin=Test&equipment_type=Dry Van",
            headers=TEST_HEADERS
        )
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)


class TestCallHandling:
    """Test call handling functionality"""
    
    @patch('src.fmcsa_service.requests.get')
    def test_start_call_valid_carrier(self, mock_get):
        """Test starting a call with valid carrier"""
        # Mock successful FMCSA API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{
                "legalName": "ABC Trucking LLC",
                "dbaName": "ABC Express",
                "entityType": "CARRIER",
                "operatingStatus": "ACTIVE",
                "outOfServiceDate": None,
                "mcs150Date": "2023-01-15",
                "mcs150Mileage": 50000,
                "phyStreet": "123 Main St",
                "phyCity": "Springfield",
                "phyState": "IL",
                "phyZipcode": "62701",
                "phyPhone": "(555) 123-4567"
            }]
        }
        mock_get.return_value = mock_response
        
        call_data = {
            "carrier_mc_number": "123456",
            "load_id": None
        }
        
        response = client.post("/api/calls/start", json=call_data, headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "call_id" in data
        assert data["carrier_verified"] is True
        
        # Verify API was called with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "123456" in call_args[0][0]  # URL contains MC number
        assert "Authorization" in call_args[1]["headers"]
    
    @patch('src.fmcsa_service.requests.get')
    def test_start_call_invalid_carrier(self, mock_get):
        """Test starting a call with invalid carrier"""
        # Mock 404 response for invalid carrier
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Carrier not found"
        mock_get.return_value = mock_response
        
        call_data = {
            "carrier_mc_number": "999999",
            "load_id": None
        }
        
        response = client.post("/api/calls/start", json=call_data, headers=TEST_HEADERS)
        assert response.status_code == 400
    
    @patch('src.fmcsa_service.requests.get')
    def test_start_call_out_of_service_carrier(self, mock_get):
        """Test starting a call with out-of-service carrier"""
        # Mock response for out-of-service carrier
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{
                "legalName": "Inactive Trucking LLC",
                "operatingStatus": "OUT-OF-SERVICE",
                "outOfServiceDate": "2023-11-01"
            }]
        }
        mock_get.return_value = mock_response
        
        call_data = {
            "carrier_mc_number": "345678",
            "load_id": None
        }
        
        response = client.post("/api/calls/start", json=call_data, headers=TEST_HEADERS)
        assert response.status_code == 400
        assert "not eligible" in response.json()["detail"]
    
    @patch('src.fmcsa_service.requests.get')
    def test_get_suitable_loads(self, mock_get):
        """Test getting suitable loads for a call"""
        # Mock successful FMCSA API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{
                "legalName": "ABC Trucking LLC",
                "operatingStatus": "ACTIVE"
            }]
        }
        mock_get.return_value = mock_response
        
        # First create a call
        call_data = {"carrier_mc_number": "123456"}
        call_response = client.post("/api/calls/start", json=call_data, headers=TEST_HEADERS)
        assert call_response.status_code == 200
        call_id = call_response.json()["call_id"]
        
        # Then get suitable loads
        response = client.get(f"/api/calls/{call_id}/loads", headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    @patch('src.fmcsa_service.requests.get')
    def test_negotiation_handling(self, mock_get):
        """Test negotiation functionality"""
        # Mock successful FMCSA API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{
                "legalName": "ABC Trucking LLC",
                "operatingStatus": "ACTIVE"
            }]
        }
        mock_get.return_value = mock_response
        
        # Create a call and load first
        call_data = {"carrier_mc_number": "123456"}
        call_response = client.post("/api/calls/start", json=call_data, headers=TEST_HEADERS)
        assert call_response.status_code == 200
        call_id = call_response.json()["call_id"]
        
        # Create a load
        import time
        unique_load_id = f"NEGO{int(time.time() * 1000)}"
        load_data = {
            "load_id": unique_load_id,
            "origin": "Negotiation Test",
            "destination": "Test Destination",
            "pickup_datetime": "2024-01-25T10:00:00Z",
            "delivery_datetime": "2024-01-26T18:00:00Z",
            "equipment_type": "Dry Van",
            "loadboard_rate": 2000.00
        }
        client.post("/api/loads", json=load_data, headers=TEST_HEADERS)
        
        # Test negotiation
        negotiation_data = {
            "call_id": call_id,
            "carrier_offer": 1900.00,
            "notes": "Test negotiation"
        }
        
        response = client.post(f"/api/calls/{call_id}/negotiate", json=negotiation_data, headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert "accepted" in data
        assert "response" in data
        assert "should_transfer" in data


class TestMetrics:
    """Test metrics and dashboard endpoints"""
    
    def test_call_metrics(self):
        """Test call metrics endpoint"""
        response = client.get("/api/metrics/calls", headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert "total_calls" in data
        assert "conversion_rate" in data
        assert "sentiment_distribution" in data
        assert "outcome_distribution" in data
    
    def test_load_metrics(self):
        """Test load metrics endpoint"""
        response = client.get("/api/metrics/loads", headers=TEST_HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        assert "total_loads" in data
        assert "available_loads" in data
        assert "average_rate" in data


class TestSecurity:
    """Test API security"""
    
    def test_missing_api_key(self):
        """Test API access without API key"""
        response = client.get("/api/loads")
        assert response.status_code == 401
    
    def test_invalid_api_key(self):
        """Test API access with invalid API key"""
        invalid_headers = {"X-API-Key": "invalid-key"}
        response = client.get("/api/loads", headers=invalid_headers)
        assert response.status_code == 401
    
    def test_valid_api_key(self):
        """Test API access with valid API key"""
        response = client.get("/api/loads", headers=TEST_HEADERS)
        assert response.status_code == 200


class TestFMCSAIntegration:
    """Test FMCSA service integration"""
    
    @pytest.mark.asyncio
    @patch('src.fmcsa_service.requests.get')
    async def test_carrier_verification_success(self, mock_get):
        """Test successful carrier verification with FMCSA API"""
        from src.fmcsa_service import FMCSAService
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{
                "legalName": "ABC Trucking LLC",
                "dbaName": "ABC Express",
                "entityType": "CARRIER",
                "operatingStatus": "ACTIVE",
                "outOfServiceDate": None,
                "mcs150Date": "2023-01-15",
                "mcs150Mileage": 50000,
                "phyStreet": "123 Main St",
                "phyCity": "Springfield",
                "phyState": "IL",
                "phyZipcode": "62701",
                "phyPhone": "(555) 123-4567"
            }]
        }
        mock_get.return_value = mock_response
        
        service = FMCSAService()
        carrier_info = await service.verify_carrier("123456")
        
        assert carrier_info is not None
        assert carrier_info.mc_number == "MC-123456"
        assert carrier_info.legal_name == "ABC Trucking LLC"
        assert carrier_info.operating_status == "ACTIVE"
        assert carrier_info.physical_address == "123 Main St, Springfield, IL, 62701"
        
        # Verify API call was made correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert settings.fmcsa_api_key in call_args[1]["headers"]["Authorization"]
    
    @pytest.mark.asyncio
    @patch('src.fmcsa_service.requests.get')
    async def test_carrier_verification_not_found(self, mock_get):
        """Test carrier verification when carrier not found"""
        from src.fmcsa_service import FMCSAService
        
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Carrier not found"
        mock_get.return_value = mock_response
        
        service = FMCSAService()
        carrier_info = await service.verify_carrier("999999")
        
        assert carrier_info is None
    
    @pytest.mark.asyncio
    @patch('src.fmcsa_service.requests.get')
    async def test_carrier_verification_network_error(self, mock_get):
        """Test carrier verification with network error fallback"""
        from src.fmcsa_service import FMCSAService
        
        # Mock network error
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        service = FMCSAService()
        carrier_info = await service.verify_carrier("123456")
        
        # Should fallback to simulation and return test data
        assert carrier_info is not None  # Falls back to simulation
        assert carrier_info.mc_number == "MC-123456"
    
    @pytest.mark.asyncio
    @patch('src.fmcsa_service.requests.get')
    async def test_carrier_verification_api_error(self, mock_get):
        """Test carrier verification with API error"""
        from src.fmcsa_service import FMCSAService
        
        # Mock API error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_get.return_value = mock_response
        
        service = FMCSAService()
        carrier_info = await service.verify_carrier("123456")
        
        # Should fallback to simulation
        assert carrier_info is not None
    
    def test_carrier_eligibility_active(self):
        """Test carrier eligibility for active carrier"""
        from src.fmcsa_service import FMCSAService
        
        service = FMCSAService()
        
        active_carrier = FMCSACarrierInfo(
            mc_number="MC-123456",
            legal_name="Test Carrier",
            entity_type="CARRIER",
            operating_status="ACTIVE"
        )
        assert service.is_carrier_eligible(active_carrier) is True
    
    def test_carrier_eligibility_out_of_service(self):
        """Test carrier eligibility for out-of-service carrier"""
        from src.fmcsa_service import FMCSAService
        
        service = FMCSAService()
        
        inactive_carrier = FMCSACarrierInfo(
            mc_number="MC-999999",
            legal_name="Inactive Carrier",
            entity_type="CARRIER",
            operating_status="OUT-OF-SERVICE"
        )
        assert service.is_carrier_eligible(inactive_carrier) is False
    
    def test_carrier_eligibility_none(self):
        """Test carrier eligibility with None input"""
        from src.fmcsa_service import FMCSAService
        
        service = FMCSAService()
        assert service.is_carrier_eligible(None) is False
    
    def test_parse_fmcsa_response(self):
        """Test FMCSA response parsing"""
        from src.fmcsa_service import FMCSAService
        
        service = FMCSAService()
        
        # Test data similar to real FMCSA response
        test_response = {
            "content": [{
                "legalName": "Test Trucking LLC",
                "dbaName": "Test Express",
                "entityType": "CARRIER",
                "operatingStatus": "ACTIVE",
                "mcs150Date": "2023-06-15",
                "mcs150Mileage": 75000,
                "phyStreet": "456 Test Ave",
                "phyCity": "Test City",
                "phyState": "TX",
                "phyZipcode": "12345",
                "phyPhone": "(555) 987-6543"
            }]
        }
        
        parsed = service._parse_fmcsa_response(test_response, "123456")
        
        assert parsed is not None
        assert parsed["mc_number"] == "MC-123456"
        assert parsed["legal_name"] == "Test Trucking LLC"
        assert parsed["operating_status"] == "ACTIVE"
        assert parsed["physical_address"] == "456 Test Ave, Test City, TX, 12345"
        assert parsed["phone"] == "(555) 987-6543"
    
    def test_format_address(self):
        """Test address formatting"""
        from src.fmcsa_service import FMCSAService
        
        service = FMCSAService()
        
        carrier_data = {
            "phyStreet": "123 Main St",
            "phyCity": "Springfield",
            "phyState": "IL",
            "phyZipcode": "62701"
        }
        
        address = service._format_address(carrier_data)
        assert address == "123 Main St, Springfield, IL, 62701"
        
        # Test partial address
        partial_data = {
            "phyCity": "Chicago",
            "phyState": "IL"
        }
        
        partial_address = service._format_address(partial_data)
        assert partial_address == "Chicago, IL"


if __name__ == "__main__":
    pytest.main([__file__])
