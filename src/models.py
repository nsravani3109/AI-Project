"""
Database models for the Inbound Sales AI Agent
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Load(Base):
    """Load model representing freight loads"""
    __tablename__ = "loads"
    
    load_id = Column(String, primary_key=True, index=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    pickup_datetime = Column(DateTime, nullable=False)
    delivery_datetime = Column(DateTime, nullable=False)
    equipment_type = Column(String, nullable=False)
    loadboard_rate = Column(Float, nullable=False)
    notes = Column(Text)
    weight = Column(Float)
    commodity_type = Column(String)
    num_of_pieces = Column(Integer)
    miles = Column(Float)
    dimensions = Column(String)
    status = Column(String, default="available")  # available, booked, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calls = relationship("Call", back_populates="load")


class Carrier(Base):
    """Carrier model for storing carrier information"""
    __tablename__ = "carriers"
    
    mc_number = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    status = Column(String)  # Active, Out-of-Service, etc.
    address = Column(Text)
    phone = Column(String)
    email = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calls = relationship("Call", back_populates="carrier")


class Call(Base):
    """Call model for storing call information and outcomes"""
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True, index=True)
    carrier_mc_number = Column(String, ForeignKey("carriers.mc_number"))
    load_id = Column(String, ForeignKey("loads.load_id"))
    call_start_time = Column(DateTime, default=datetime.utcnow)
    call_end_time = Column(DateTime)
    call_duration = Column(Integer)  # in seconds
    outcome = Column(String)  # accepted, rejected, negotiating, transferred
    sentiment = Column(String)  # positive, neutral, negative
    initial_rate_offered = Column(Float)
    final_rate_agreed = Column(Float)
    negotiation_rounds = Column(Integer, default=0)
    notes = Column(Text)
    call_transcript = Column(Text)
    transferred_to_rep = Column(Boolean, default=False)
    
    # Relationships
    carrier = relationship("Carrier", back_populates="calls")
    load = relationship("Load", back_populates="calls")
    
    # Negotiation history
    negotiations = relationship("Negotiation", back_populates="call")


class Negotiation(Base):
    """Negotiation model for tracking negotiation rounds"""
    __tablename__ = "negotiations"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.id"))
    session_id = Column(String, nullable=True, index=True)  # Session identifier for grouping negotiations
    round_number = Column(Integer, nullable=False)
    carrier_offer = Column(Float)
    system_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    call = relationship("Call", back_populates="negotiations")
