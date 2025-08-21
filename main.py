"""
Main FastAPI application for Inbound Sales AI Agent
"""
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import logging
from datetime import datetime

# Local imports
from config.settings import settings
from src.database import get_db
from src.schemas import *
from src.models import Load, Carrier, Call
from src.call_service import CallHandlingService
from src.load_service import LoadService
from src.security import get_api_key_from_header

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Inbound Sales AI Agent",
    description="AI-powered inbound carrier sales automation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "Inbound Sales AI Agent API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.utcnow()
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "fmcsa": "available",
            "load_matching": "active",
            "call_handling": "active"
        }
    }


# Load Management Endpoints
@app.post("/api/loads", response_model=LoadResponse)
def create_load(
    load: LoadCreate,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Create a new freight load"""
    get_api_key_from_header(api_key)
    
    load_service = LoadService(db)
    db_load = load_service.create_load(load)
    return db_load


@app.get("/api/loads", response_model=List[LoadResponse])
def get_loads(
    limit: int = 100,
    status: Optional[LoadStatus] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get available loads"""
    get_api_key_from_header(api_key)
    
    load_service = LoadService(db)
    if status:
        loads = db.query(Load).filter(Load.status == status).limit(limit).all()
    else:
        loads = load_service.get_available_loads(limit)
    
    return loads


@app.post("/api/loads/search", response_model=List[LoadResponse])
def search_loads(
    search_criteria: LoadSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Search for loads based on criteria"""
    get_api_key_from_header(api_key)
    
    load_service = LoadService(db)
    loads = load_service.search_loads(
        origin=search_criteria.origin,
        destination=search_criteria.destination,
        equipment_type=search_criteria.equipment_type,
        min_rate=search_criteria.min_rate,
        max_rate=search_criteria.max_rate,
        limit=search_criteria.limit
    )
    return loads


@app.get("/api/loads/{load_id}", response_model=LoadResponse)
def get_load(
    load_id: str,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get a specific load"""
    get_api_key_from_header(api_key)
    
    load_service = LoadService(db)
    load = load_service.get_load(load_id)
    if not load:
        raise HTTPException(status_code=404, detail="Load not found")
    return load


# Call Handling Endpoints
@app.post("/api/validate_mc")
async def start_call(
    call_data: CallStart,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Start a new carrier call"""
    get_api_key_from_header(api_key)
    
    call_service = CallHandlingService(db)
    success, message, call = await call_service.start_call(call_data)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "call_id": call.id,
        "carrier_verified": True
    }


@app.get("/api/calls/{call_id}/loads", response_model=List[LoadResponse])
def get_suitable_loads(
    call_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get suitable loads for an active call"""
    get_api_key_from_header(api_key)
    
    call_service = CallHandlingService(db)
    loads = call_service.find_and_pitch_loads(call_id)
    
    if not loads:
        return {"message": "No suitable loads found at this time", "loads": []}
    
    return loads


@app.post("/api/calls/{call_id}/negotiate")
def handle_negotiation(
    call_id: str,
    offer: NegotiationOffer,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Handle negotiation round"""
    get_api_key_from_header(api_key)
    
    call_service = CallHandlingService(db)
    accepted, response, should_transfer = call_service.handle_negotiation(
        call_id, offer.carrier_offer, offer.session_id
    )
    
    return {
        "accepted": accepted,
        "response": response,
        "should_transfer": should_transfer,
        "negotiation_round": call_service.db.query(Call).filter(Call.id == call_id).first().negotiation_rounds
    }


@app.post("/api/calls/{call_id}/end")
def end_call(
    call_id: int,
    call_update: CallUpdate,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """End a call"""
    get_api_key_from_header(api_key)
    
    call_service = CallHandlingService(db)
    call_service.end_call(
        call_id,
        call_update.outcome,
        call_update.sentiment,
        call_update.notes
    )
    
    return {"message": "Call ended successfully"}


@app.get("/api/calls/{call_id}", response_model=CallResponse)
def get_call(
    call_id: int,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get call details"""
    get_api_key_from_header(api_key)
    
    call = db.query(Call).filter(Call.id == call_id).first()
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    return call


@app.get("/api/negotiations/session/{session_id}", response_model=List[NegotiationResponse])
def get_negotiations_by_session(
    session_id: str,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get all negotiations for a specific session"""
    get_api_key_from_header(api_key)
    
    from src.models import Negotiation
    negotiations = db.query(Negotiation).filter(
        Negotiation.session_id == session_id
    ).order_by(Negotiation.timestamp).all()
    
    if not negotiations:
        raise HTTPException(status_code=404, detail=f"No negotiations found for session {session_id}")
    
    return negotiations


@app.get("/api/calls/{call_id}/negotiations", response_model=List[NegotiationResponse]) 
def get_negotiations_by_call(
    call_id: int,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get negotiations for a specific call, optionally filtered by session"""
    get_api_key_from_header(api_key)
    
    from src.models import Negotiation
    query = db.query(Negotiation).filter(Negotiation.call_id == call_id)
    
    if session_id:
        query = query.filter(Negotiation.session_id == session_id)
    
    negotiations = query.order_by(Negotiation.timestamp).all()
    
    return negotiations


# Carrier Management Endpoints
@app.get("/api/carriers/{mc_number}", response_model=CarrierResponse)
def get_carrier(
    mc_number: str,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get carrier information"""
    get_api_key_from_header(api_key)
    
    carrier = db.query(Carrier).filter(Carrier.mc_number == mc_number).first()
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    
    return carrier


# HappyRobot Webhook Endpoint
@app.post("/api/webhook/happyrobot")
def happyrobot_webhook(
    webhook_data: HappyRobotWebhook,
    db: Session = Depends(get_db)
):
    """Handle HappyRobot webhooks"""
    logger.info(f"Received HappyRobot webhook: {webhook_data}")
    
    # Process webhook data
    # Update call records with transcript and status
    
    return {"status": "processed"}


# Metrics and Dashboard Endpoints
@app.get("/api/metrics/calls", response_model=CallMetrics)
def get_call_metrics(
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get call metrics for dashboard"""
    get_api_key_from_header(api_key)
    
    total_calls = db.query(Call).count()
    successful_bookings = db.query(Call).filter(Call.outcome == CallOutcome.ACCEPTED).count()
    conversion_rate = (successful_bookings / total_calls * 100) if total_calls > 0 else 0
    
    # Calculate average negotiation rounds
    avg_negotiation_rounds = db.query(Call).filter(Call.negotiation_rounds > 0).with_entities(
        func.avg(Call.negotiation_rounds)
    ).scalar() or 0
    
    # Sentiment distribution
    sentiment_counts = db.query(Call.sentiment, func.count(Call.id)).filter(
        Call.sentiment.isnot(None)
    ).group_by(Call.sentiment).all()
    sentiment_distribution = {sentiment: count for sentiment, count in sentiment_counts}
    
    # Outcome distribution
    outcome_counts = db.query(Call.outcome, func.count(Call.id)).filter(
        Call.outcome.isnot(None)
    ).group_by(Call.outcome).all()
    outcome_distribution = {outcome: count for outcome, count in outcome_counts}
    
    return CallMetrics(
        total_calls=total_calls,
        successful_bookings=successful_bookings,
        conversion_rate=conversion_rate,
        average_negotiation_rounds=float(avg_negotiation_rounds),
        sentiment_distribution=sentiment_distribution,
        outcome_distribution=outcome_distribution
    )


@app.get("/api/metrics/loads", response_model=LoadMetrics)
def get_load_metrics(
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="X-API-Key")
):
    """Get load metrics for dashboard"""
    get_api_key_from_header(api_key)
    
    total_loads = db.query(Load).count()
    available_loads = db.query(Load).filter(Load.status == LoadStatus.AVAILABLE).count()
    booked_loads = db.query(Load).filter(Load.status == LoadStatus.BOOKED).count()
    completed_loads = db.query(Load).filter(Load.status == LoadStatus.COMPLETED).count()
    
    # Calculate average rate
    avg_rate = db.query(Load).with_entities(func.avg(Load.loadboard_rate)).scalar() or 0
    
    return LoadMetrics(
        total_loads=total_loads,
        available_loads=available_loads,
        booked_loads=booked_loads,
        completed_loads=completed_loads,
        average_rate=float(avg_rate)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
