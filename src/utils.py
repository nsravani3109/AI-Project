"""
Utility functions for the Inbound Sales AI Agent
"""
import uuid
import string
import random
from datetime import datetime


def generate_session_id(prefix: str = "sess") -> str:
    """
    Generate a unique session ID
    
    Args:
        prefix: Prefix for the session ID (default: "sess")
        
    Returns:
        Unique session ID string
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{timestamp}_{random_part}"


def generate_uuid_session_id() -> str:
    """
    Generate a UUID-based session ID
    
    Returns:
        UUID-based session ID string
    """
    return f"sess_{str(uuid.uuid4()).replace('-', '')[:16]}"


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not session_id:
        return False
    
    # Basic validation - should start with sess_ and have reasonable length
    return (
        session_id.startswith("sess_") and 
        len(session_id) >= 10 and 
        len(session_id) <= 50
    )


def format_session_response(session_id: str, call_id: int, load_id: str = None) -> dict:
    """
    Format session response data
    
    Args:
        session_id: Session identifier
        call_id: Call identifier
        load_id: Optional load identifier
        
    Returns:
        Formatted session data
    """
    response = {
        "session_id": session_id,
        "call_id": call_id,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": None  # Can be implemented later
    }
    
    if load_id:
        response["load_id"] = load_id
        
    return response
