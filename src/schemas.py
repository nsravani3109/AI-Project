"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CallOutcome(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEGOTIATING = "negotiating"
    TRANSFERRED = "transferred"
    ABANDONED = "abandoned"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class LoadStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    COMPLETED = "completed"


# Load Schemas
class LoadBase(BaseModel):
    origin: str
    destination: str
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str
    loadboard_rate: float
    notes: Optional[str] = None
    weight: Optional[float] = None
    commodity_type: Optional[str] = None
    num_of_pieces: Optional[int] = None
    miles: Optional[float] = None
    dimensions: Optional[str] = None


class LoadCreate(LoadBase):
    load_id: str


class LoadResponse(LoadBase):
    load_id: str
    status: LoadStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoadSearchRequest(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    equipment_type: Optional[str] = None
    min_rate: Optional[float] = None
    max_rate: Optional[float] = None
    limit: int = Field(default=10, ge=1, le=100)

    class Config:
        from_attributes = True


# Carrier Schemas
class CarrierBase(BaseModel):
    company_name: str
    status: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class CarrierCreate(CarrierBase):
    mc_number: str


class CarrierResponse(CarrierBase):
    mc_number: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Call Schemas
class CallStart(BaseModel):
    carrier_mc_number: str
    load_id: Optional[str] = None


class NegotiationOffer(BaseModel):
    call_id: str
    carrier_offer: float
    session_id: Optional[str] = None  # Optional session identifier
    notes: Optional[str] = None


class NegotiationResponse(BaseModel):
    id: int
    call_id: int
    session_id: Optional[str]
    round_number: int
    carrier_offer: Optional[float]
    system_response: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class CallUpdate(BaseModel):
    outcome: Optional[CallOutcome] = None
    sentiment: Optional[Sentiment] = None
    final_rate_agreed: Optional[float] = None
    notes: Optional[str] = None
    transferred_to_rep: Optional[bool] = None


class CallResponse(BaseModel):
    id: int
    carrier_mc_number: str
    load_id: Optional[str]
    call_start_time: datetime
    call_end_time: Optional[datetime]
    call_duration: Optional[int]
    outcome: Optional[CallOutcome]
    sentiment: Optional[Sentiment]
    initial_rate_offered: Optional[float]
    final_rate_agreed: Optional[float]
    negotiation_rounds: int
    transferred_to_rep: bool

    class Config:
        from_attributes = True


# FMCSA API Response
class FMCSACarrierInfo(BaseModel):
    mc_number: str
    legal_name: str
    dba_name: Optional[str] = None
    entity_type: str
    operating_status: str
    out_of_service_date: Optional[str] = None
    mcs_150_date: Optional[str] = None
    mcs_150_mileage: Optional[int] = None
    physical_address: Optional[str] = None
    phone: Optional[str] = None


# Dashboard Schemas
class CallMetrics(BaseModel):
    total_calls: int
    successful_bookings: int
    conversion_rate: float
    average_negotiation_rounds: float
    sentiment_distribution: dict
    outcome_distribution: dict


class LoadMetrics(BaseModel):
    total_loads: int
    available_loads: int
    booked_loads: int
    completed_loads: int
    average_rate: float


# HappyRobot Integration
class HappyRobotWebhook(BaseModel):
    call_id: str
    carrier_mc_number: str
    transcript: Optional[str] = None
    call_status: str
    metadata: Optional[dict] = None
