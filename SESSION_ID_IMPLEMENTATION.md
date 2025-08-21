# Session ID Implementation Guide

## Overview

The `session_id` column has been added to the `negotiations` table to provide better session management and grouping of related negotiation rounds. This enables tracking of negotiation sessions independently of call records.

## Database Changes

### New Column
- **Table**: `negotiations`
- **Column**: `session_id` (TEXT, nullable, indexed)
- **Purpose**: Groups related negotiation rounds within a session

### Indexes Added
```sql
CREATE INDEX idx_negotiations_session_id ON negotiations(session_id);
CREATE INDEX idx_negotiations_call_session ON negotiations(call_id, session_id);
```

## API Changes

### Updated Schemas

#### NegotiationOffer
```python
class NegotiationOffer(BaseModel):
    call_id: str
    carrier_offer: float
    session_id: Optional[str] = None  # NEW: Optional session identifier
    notes: Optional[str] = None
```

#### New NegotiationResponse
```python
class NegotiationResponse(BaseModel):
    id: int
    call_id: int
    session_id: Optional[str]  # NEW
    round_number: int
    carrier_offer: Optional[float]
    system_response: Optional[str]
    timestamp: datetime
```

### New API Endpoints

#### 1. Get Negotiations by Session
```http
GET /api/negotiations/session/{session_id}
```
**Purpose**: Retrieve all negotiations for a specific session
**Response**: List of NegotiationResponse objects

#### 2. Get Call Negotiations (Enhanced)
```http
GET /api/calls/{call_id}/negotiations?session_id={optional_session_id}
```
**Purpose**: Get negotiations for a call, optionally filtered by session
**Response**: List of NegotiationResponse objects

### Updated Service Methods

#### CallHandlingService.handle_negotiation()
```python
def handle_negotiation(self, call_id: str, carrier_offer: float, session_id: Optional[str] = None) -> Tuple[bool, str, bool]:
```
- **New Parameter**: `session_id` (optional)
- **Behavior**: Stores session_id in negotiation records

## Usage Examples

### 1. Starting a Negotiation Session
```python
# Generate session ID
from src.utils import generate_session_id
session_id = generate_session_id()  # Returns: "sess_20250820224530_abc123"

# Make negotiation request
response = requests.post(
    f"http://localhost:8000/api/calls/{call_id}/negotiate",
    headers={"X-API-Key": "default-api-key"},
    json={
        "call_id": "123",
        "carrier_offer": 2300.00,
        "session_id": session_id,
        "notes": "Initial offer"
    }
)
```

### 2. Continuing a Session
```python
# Use same session_id for subsequent negotiations
response = requests.post(
    f"http://localhost:8000/api/calls/{call_id}/negotiate",
    headers={"X-API-Key": "default-api-key"},
    json={
        "call_id": "123",
        "carrier_offer": 2250.00,
        "session_id": session_id,  # Same session
        "notes": "Counter offer"
    }
)
```

### 3. Retrieving Session History
```python
# Get all negotiations in a session
response = requests.get(
    f"http://localhost:8000/api/negotiations/session/{session_id}",
    headers={"X-API-Key": "default-api-key"}
)

negotiations = response.json()
# Returns chronological list of all negotiations in this session
```

## Utility Functions

### Session ID Generation
```python
from src.utils import generate_session_id, generate_uuid_session_id

# Timestamp-based (recommended)
session_id = generate_session_id()  # "sess_20250820224530_abc123"

# UUID-based
session_id = generate_uuid_session_id()  # "sess_a1b2c3d4e5f6g7h8"
```

### Session Validation
```python
from src.utils import validate_session_id

is_valid = validate_session_id("sess_20250820224530_abc123")  # True
is_valid = validate_session_id("invalid")  # False
```

## Benefits

### 1. **Session Grouping**
- Group related negotiation rounds logically
- Track negotiation sessions independently of call records
- Better analytics and reporting capabilities

### 2. **Improved Tracking**
- Identify negotiation patterns within sessions
- Better debugging and audit trails
- Enhanced user experience tracking

### 3. **Flexible Architecture**
- Optional field maintains backward compatibility
- Can be used for future session-based features
- Supports multiple concurrent negotiations per call

### 4. **Performance**
- Indexed fields for fast queries
- Efficient session-based filtering
- Optimized for analytics queries

## Migration

### Automatic Migration
```bash
# Run migration script
./migrate_add_session_id.sh loads.db

# Backup is automatically created
# New indexes are automatically added
```

### Manual Migration
```sql
-- Add column
ALTER TABLE negotiations ADD COLUMN session_id TEXT;

-- Add indexes
CREATE INDEX idx_negotiations_session_id ON negotiations(session_id);
CREATE INDEX idx_negotiations_call_session ON negotiations(call_id, session_id);
```

## Best Practices

### 1. **Session ID Management**
- Generate session IDs at the client side
- Include timestamp for chronological sorting
- Use consistent prefix ("sess_") for identification

### 2. **API Usage**
- Always include session_id for related negotiations
- Use the same session_id for continuation calls
- Retrieve session history for context

### 3. **Database Queries**
- Use session_id for grouping negotiations
- Combine with call_id for specific session within call
- Order by timestamp for chronological view

### 4. **Error Handling**
- Validate session_id format before processing
- Handle missing session_id gracefully (optional field)
- Provide meaningful error messages for invalid sessions

## Future Enhancements

### Potential Extensions
1. **Session Expiration**: Add expiration timestamps
2. **Session Status**: Track session states (active, completed, expired)
3. **Session Metadata**: Store additional session context
4. **Cross-Call Sessions**: Link sessions across multiple calls
5. **Session Analytics**: Advanced reporting and insights

This implementation provides a solid foundation for session-based negotiation tracking while maintaining backward compatibility and performance.
