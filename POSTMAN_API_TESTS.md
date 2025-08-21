# Postman API Test Collection - Inbound Sales AI Agent

## Base Configuration
- **Base URL**: `http://localhost:8000`
- **Required Header**: `X-API-Key: default-api-key`
- **Content-Type**: `application/json`

## 1. Health Check Endpoints

### 1.1 Root Health Check
```http
GET http://localhost:8000/
```
**Headers**: None required
**Expected Response**: 200 OK
```json
{
    "message": "Inbound Sales AI Agent API",
    "version": "1.0.0",
    "status": "active",
    "timestamp": "2025-08-19T10:30:00.000Z"
}
```

### 1.2 Detailed Health Check
```http
GET http://localhost:8000/health
```
**Headers**: None required
**Expected Response**: 200 OK
```json
{
    "status": "healthy",
    "database": "connected",
    "services": {
        "fmcsa": "available",
        "load_matching": "active",
        "call_handling": "active"
    }
}
```

## 2. Load Management Endpoints

### 2.1 Create Load
```http
POST http://localhost:8000/api/loads
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "load_id": "LOAD001",
    "origin": "Chicago, IL",
    "destination": "Atlanta, GA",
    "pickup_datetime": "2025-08-25T08:00:00Z",
    "delivery_datetime": "2025-08-26T17:00:00Z",
    "equipment_type": "Dry Van",
    "loadboard_rate": 2500.00,
    "notes": "High priority shipment",
    "weight": 42000,
    "commodity_type": "Electronics",
    "num_of_pieces": 25,
    "miles": 588,
    "dimensions": "53' x 8.5' x 9'"
}
```

### 2.2 Create Another Load (Different Route)
```http
POST http://localhost:8000/api/loads
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "load_id": "LOAD002",
    "origin": "Los Angeles, CA",
    "destination": "Dallas, TX",
    "pickup_datetime": "2025-08-27T10:00:00Z",
    "delivery_datetime": "2025-08-28T16:00:00Z",
    "equipment_type": "Reefer",
    "loadboard_rate": 3200.00,
    "notes": "Temperature controlled freight",
    "weight": 38000,
    "commodity_type": "Food Products",
    "num_of_pieces": 18,
    "miles": 1435,
    "dimensions": "53' x 8.5' x 9'"
}
```

### 2.3 Get All Loads
```http
GET http://localhost:8000/api/loads
```
**Headers**:
```
X-API-Key: default-api-key
```
**Query Parameters** (optional):
- `limit=10`
- `status=AVAILABLE`

### 2.4 Get Loads with Filters
```http
GET http://localhost:8000/api/loads?limit=5&status=AVAILABLE
```
**Headers**:
```
X-API-Key: default-api-key
```

### 2.5 Search Loads
```http
POST http://localhost:8000/api/loads/search
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
  "origin": "Chicago",
  "equipment_type": "Dry Van",
  "min_rate": 2000,
  "max_rate": 3000,
  "limit": 5
}
```

### 2.6 Get Specific Load
```http
GET http://localhost:8000/api/loads/LOAD001
```
**Headers**:
```
X-API-Key: default-api-key
```

## 3. Call Handling Endpoints

### 3.1 Start Call (Valid Carrier)
```http
POST http://localhost:8000/api/calls/start
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "mc_number": "243563"
}
```

### 3.2 Start Call (Different Carrier)
```http
POST http://localhost:8000/api/calls/start
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "mc_number": "123456"
}
```

### 3.3 Get Suitable Loads for Call
```http
GET http://localhost:8000/api/calls/1/loads
```
**Headers**:
```
X-API-Key: default-api-key
```
**Note**: Replace `1` with actual call_id from start_call response

### 3.4 Handle Negotiation
```http
POST http://localhost:8000/api/loads/LD001/negotiate
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "carrier_mc_number": "MC123456",
    "carrier_offer": 2300.00,
    "notes": "Need higher rate due to fuel costs"
}
```

### 3.5 Handle Counter Negotiation
```http
POST http://localhost:8000/api/loads/LD001/negotiate
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "carrier_mc_number": "MC123456",
    "carrier_offer": 2450.00,
    "notes": "Final counter offer"
}
```

### 3.6 End Call
```http
POST http://localhost:8000/api/calls/1/end
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{
    "outcome": "ACCEPTED",
    "sentiment": "POSITIVE",
    "notes": "Carrier accepted the load after negotiation"
}
```

### 3.7 Get Call Details
```http
GET http://localhost:8000/api/calls/1
```
**Headers**:
```
X-API-Key: default-api-key
```

## 4. Carrier Management Endpoints

### 4.1 Get Carrier Info
```http
GET http://localhost:8000/api/carriers/243563
```
**Headers**:
```
X-API-Key: default-api-key
```

### 4.2 Get Different Carrier
```http
GET http://localhost:8000/api/carriers/123456
```
**Headers**:
```
X-API-Key: default-api-key
```

## 5. Metrics Endpoints

### 5.1 Get Call Metrics
```http
GET http://localhost:8000/api/metrics/calls
```
**Headers**:
```
X-API-Key: default-api-key
```

### 5.2 Get Load Metrics
```http
GET http://localhost:8000/api/metrics/loads
```
**Headers**:
```
X-API-Key: default-api-key
```

## 6. Webhook Endpoints

### 6.1 HappyRobot Webhook (Simulated)
```http
POST http://localhost:8000/api/webhook/happyrobot
```
**Headers**:
```
Content-Type: application/json
```
**Body**:
```json
{
    "call_id": "hr_call_123",
    "event_type": "call_started",
    "transcript": "Hello, this is John from ABC Trucking, MC number 243563",
    "sentiment": "neutral",
    "timestamp": "2025-08-19T10:30:00Z"
}
```

## 7. Error Testing Scenarios

### 7.1 Missing API Key
```http
GET http://localhost:8000/api/loads
```
**Headers**: None (omit X-API-Key)
**Expected Response**: 401 Unauthorized

### 7.2 Invalid API Key
```http
GET http://localhost:8000/api/loads
```
**Headers**:
```
X-API-Key: invalid-key
```
**Expected Response**: 401 Unauthorized

### 7.3 Load Not Found
```http
GET http://localhost:8000/api/loads/NONEXISTENT
```
**Headers**:
```
X-API-Key: default-api-key
```
**Expected Response**: 404 Not Found

### 7.4 Carrier Not Found
```http
GET http://localhost:8000/api/carriers/999999
```
**Headers**:
```
X-API-Key: default-api-key
```
**Expected Response**: 404 Not Found

### 7.5 Invalid Call Start (Missing MC Number)
```http
POST http://localhost:8000/api/calls/start
```
**Headers**:
```
X-API-Key: default-api-key
Content-Type: application/json
```
**Body**:
```json
{}
```
**Expected Response**: 422 Validation Error

## 8. Test Sequence Workflow

### Complete Call Flow Test:
1. **Create Load** → Use 2.1 (note the load_id, e.g., "LD001")
2. **Start Call** → Use 3.1 (note the call_id)
3. **Get Suitable Loads** → Use 3.3 (with call_id from step 2)
4. **Negotiate** → Use 3.4 (with load_id from step 1, include carrier_mc_number)
5. **Counter Negotiate** → Use 3.5 (with load_id, include carrier_mc_number)
6. **End Call** → Use 3.6 (with call_id)
7. **Get Call Details** → Use 3.7 (with call_id)
8. **Check Metrics** → Use 5.1 and 5.2

## 9. Dashboard Access

### 9.1 Access Dashboard
```
Open Browser: http://localhost:8050/
```
This opens the Dash analytics dashboard

## 10. API Documentation

### 10.1 OpenAPI Docs
```
Open Browser: http://localhost:8000/docs
```

### 10.2 ReDoc Documentation
```
Open Browser: http://localhost:8000/redoc
```

## Environment Variables for Testing

Make sure these are set in your `.env` file or environment:
```bash
API_KEY=default-api-key
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./loads.db
DEBUG=True
FMCSA_API_KEY=cdc33e44d693a3a58451898d4ec9df862c65b954
HAPPYROBOT_API_KEY=your-happyrobot-api-key
```

## Testing Tips

1. **Start the server first**:
   ```bash
   cd /Users/sivakrishna/Downloads/InboundSalesAiAgent
   source venv/bin/activate
   python main.py
   ```

2. **Import in Postman**:
   - Create a new collection
   - Add environment variables for base_url and api_key
   - Copy each request above

3. **Test in Order**:
   - Start with health checks
   - Create loads first
   - Then test call handling
   - Check metrics last

4. **Monitor Logs**:
   - Watch console output for FMCSA API calls
   - Check database updates after each operation

This comprehensive test suite covers all endpoints and common error scenarios!
