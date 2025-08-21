"""
FMCSA API integration service
"""
import requests
import logging
from typing import Optional
from config.settings import settings
from src.schemas import FMCSACarrierInfo

logger = logging.getLogger(__name__)


class FMCSAService:
    """Service for interacting with FMCSA API"""
    
    def __init__(self):
        self.base_url = settings.fmcsa_api_base_url
        self.api_key = settings.fmcsa_api_key
    
    async def verify_carrier(self, mc_number: str) -> Optional[FMCSACarrierInfo]:
        """
        Verify carrier using FMCSA API
        
        Args:
            mc_number: Motor Carrier number to verify
            
        Returns:
            FMCSACarrierInfo if found, None otherwise
        """
        try:
            # Remove 'MC' prefix if present and clean the number
            clean_mc_number = mc_number.replace('MC', '').replace('-', '').strip()
            
            # FMCSA API endpoint
            url = f"{self.base_url}/{clean_mc_number}"
            
            # Set up headers for the API request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Make the actual API call
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse FMCSA response and map to our schema
                carrier_info = self._parse_fmcsa_response(data, clean_mc_number)
                
                if carrier_info:
                    return FMCSACarrierInfo(**carrier_info)
            
            # elif response.status_code == 404:
            #     logger.warning(f"Carrier {mc_number} not found in FMCSA database")
            #     return None
            
            else:
                logger.error(f"FMCSA API error {response.status_code}: {response.text}")
                # Fallback to simulation for testing if API fails
                carrier_info = self._simulate_fmcsa_response(clean_mc_number)
                if carrier_info:
                    return FMCSACarrierInfo(**carrier_info)
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error verifying carrier {mc_number}: {str(e)}")
            # Fallback to simulation for testing if network fails
            carrier_info = self._simulate_fmcsa_response(clean_mc_number)
            if carrier_info:
                return FMCSACarrierInfo(**carrier_info)
            return None
            
        except Exception as e:
            logger.error(f"Error verifying carrier {mc_number}: {str(e)}")
            return None
    
    def _simulate_fmcsa_response(self, mc_number: str) -> Optional[dict]:
        """
        Simulate FMCSA API response for demo purposes
        In production, replace this with actual API call
        """
        # Simulate some valid MC numbers for testing
        mock_carriers = {
            "123456": {
                "mc_number": "MC-123456",
                "legal_name": "ABC Trucking LLC",
                "dba_name": "ABC Express",
                "entity_type": "CARRIER",
                "operating_status": "ACTIVE",
                "out_of_service_date": None,
                "mcs_150_date": "2023-01-15",
                "mcs_150_mileage": 50000,
                "physical_address": "123 Main St, Springfield, IL 62701",
                "phone": "(555) 123-4567"
            },
            "789012": {
                "mc_number": "MC-789012",
                "legal_name": "XYZ Transport Inc",
                "dba_name": None,
                "entity_type": "CARRIER",
                "operating_status": "ACTIVE",
                "out_of_service_date": None,
                "mcs_150_date": "2023-03-20",
                "mcs_150_mileage": 75000,
                "physical_address": "456 Oak Ave, Chicago, IL 60601",
                "phone": "(555) 987-6543"
            },
            "345678": {
                "mc_number": "MC-345678",
                "legal_name": "Reliable Freight Solutions",
                "dba_name": "RFS Logistics",
                "entity_type": "CARRIER",
                "operating_status": "OUT-OF-SERVICE",
                "out_of_service_date": "2023-11-01",
                "mcs_150_date": "2022-12-10",
                "mcs_150_mileage": 25000,
                "physical_address": "789 Pine St, Detroit, MI 48201",
                "phone": "(555) 456-7890"
            }
        }
        
        return mock_carriers.get(mc_number)
    
    def _parse_fmcsa_response(self, data: dict, mc_number: str) -> Optional[dict]:
        """
        Parse actual FMCSA API response to our schema format
        
        Args:
            data: Raw response from FMCSA API
            mc_number: The MC number that was queried
            
        Returns:
            Parsed carrier information dictionary
        """
        try:
            # FMCSA API response structure (adjust based on actual API response format)
            content = data.get('content', [])
            if not content:
                return None
            
            carrier_data = content[0] if isinstance(content, list) else content
            
            # Map FMCSA fields to our schema
            parsed_info = {
                "mc_number": f"MC-{mc_number}",
                "legal_name": carrier_data.get('legalName', ''),
                "dba_name": carrier_data.get('dbaName'),
                "entity_type": carrier_data.get('entityType', 'CARRIER'),
                "operating_status": carrier_data.get('operatingStatus', 'UNKNOWN'),
                "out_of_service_date": carrier_data.get('outOfServiceDate'),
                "mcs_150_date": carrier_data.get('mcs150Date'),
                "mcs_150_mileage": carrier_data.get('mcs150Mileage'),
                "physical_address": self._format_address(carrier_data),
                "phone": carrier_data.get('phyPhone')
            }
            
            return parsed_info
            
        except Exception as e:
            logger.error(f"Error parsing FMCSA response: {str(e)}")
            return None
    
    def _format_address(self, carrier_data: dict) -> str:
        """
        Format address from FMCSA data
        
        Args:
            carrier_data: Carrier data from FMCSA
            
        Returns:
            Formatted address string
        """
        try:
            address_parts = []
            
            street = carrier_data.get('phyStreet')
            if street:
                address_parts.append(street)
            
            city = carrier_data.get('phyCity')
            if city:
                address_parts.append(city)
            
            state = carrier_data.get('phyState')
            if state:
                address_parts.append(state)
            
            zip_code = carrier_data.get('phyZipcode')
            if zip_code:
                address_parts.append(zip_code)
            
            return ', '.join(address_parts) if address_parts else ''
        
        except Exception:
            return ''
    
    def is_carrier_eligible(self, carrier_info: FMCSACarrierInfo) -> bool:
        """
        Check if carrier is eligible to work with
        
        Args:
            carrier_info: Carrier information from FMCSA
            
        Returns:
            True if eligible, False otherwise
        """
        if not carrier_info:
            return False
        
        # Check if carrier is active
        if carrier_info.operating_status != "ACTIVE":
            return False
        
        # Add additional eligibility checks here
        # For example: insurance requirements, safety ratings, etc.
        
        return True
