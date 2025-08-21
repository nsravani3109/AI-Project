"""
Load management service
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.models import Load, Call
from src.schemas import LoadCreate, LoadResponse, LoadStatus
import logging

logger = logging.getLogger(__name__)


class LoadService:
    """Service for managing freight loads"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_load(self, load_data: LoadCreate) -> Load:
        """Create a new load"""
        db_load = Load(**load_data.model_dump())
        self.db.add(db_load)
        self.db.commit()
        self.db.refresh(db_load)
        return db_load
    
    def get_load(self, load_id: str) -> Optional[Load]:
        """Get a load by ID"""
        return self.db.query(Load).filter(Load.load_id == load_id).first()
    
    def get_available_loads(self, limit: int = 100) -> List[Load]:
        """Get all available loads"""
        return self.db.query(Load).filter(
            Load.status == LoadStatus.AVAILABLE
        ).limit(limit).all()
    
    def search_loads(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        equipment_type: Optional[str] = None,
        min_rate: Optional[float] = None,
        max_rate: Optional[float] = None,
        limit: int = 10
    ) -> List[Load]:
        """
        Search for loads based on criteria
        
        Args:
            origin: Origin location filter
            destination: Destination location filter
            equipment_type: Equipment type filter
            min_rate: Minimum rate filter
            max_rate: Maximum rate filter
            limit: Maximum number of results
            
        Returns:
            List of matching loads
        """
        query = self.db.query(Load).filter(Load.status == LoadStatus.AVAILABLE)
        
        if origin:
            query = query.filter(Load.origin.ilike(f"%{origin}%"))
        
        if destination:
            query = query.filter(Load.destination.ilike(f"%{destination}%"))
        
        if equipment_type:
            query = query.filter(Load.equipment_type == equipment_type)
        
        if min_rate:
            query = query.filter(Load.loadboard_rate >= min_rate)
        
        if max_rate:
            query = query.filter(Load.loadboard_rate <= max_rate)
        
        return query.limit(limit).all()
    
    def find_suitable_loads_for_carrier(
        self,
        carrier_mc_number: str,
        preferred_origin: Optional[str] = None,
        preferred_destination: Optional[str] = None,
        equipment_types: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[Load]:
        """
        Find suitable loads for a specific carrier
        
        Args:
            carrier_mc_number: Carrier's MC number
            preferred_origin: Preferred origin location
            preferred_destination: Preferred destination location
            equipment_types: List of equipment types the carrier can handle
            limit: Maximum number of results
            
        Returns:
            List of suitable loads
        """
        query = self.db.query(Load).filter(Load.status == LoadStatus.AVAILABLE)
        
        # Filter by equipment types if provided
        if equipment_types:
            query = query.filter(Load.equipment_type.in_(equipment_types))
        
        # Filter by preferred locations if provided
        if preferred_origin:
            query = query.filter(Load.origin.ilike(f"%{preferred_origin}%"))
        
        if preferred_destination:
            query = query.filter(Load.destination.ilike(f"%{preferred_destination}%"))
        
        # Order by rate (highest first) and pickup date
        query = query.order_by(Load.loadboard_rate.desc(), Load.pickup_datetime)
        
        return query.limit(limit).all()
    
    def update_load_status(self, load_id: str, status: LoadStatus) -> Optional[Load]:
        """Update load status"""
        load = self.get_load(load_id)
        if load:
            load.status = status
            load.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(load)
        return load
    
    def book_load(self, load_id: str, carrier_mc_number: str, agreed_rate: float) -> bool:
        """
        Book a load for a carrier
        
        Args:
            load_id: Load to book
            carrier_mc_number: Carrier booking the load
            agreed_rate: Agreed rate for the load
            
        Returns:
            True if successfully booked, False otherwise
        """
        try:
            load = self.get_load(load_id)
            if not load or load.status != LoadStatus.AVAILABLE:
                return False
            
            # Update load status
            load.status = LoadStatus.BOOKED
            load.updated_at = datetime.utcnow()
            
            # You might want to create a booking record here
            # and update the call record with the final agreed rate
            
            self.db.commit()
            logger.info(f"Load {load_id} booked by carrier {carrier_mc_number} at rate ${agreed_rate}")
            return True
            
        except Exception as e:
            logger.error(f"Error booking load {load_id}: {str(e)}")
            self.db.rollback()
            return False
