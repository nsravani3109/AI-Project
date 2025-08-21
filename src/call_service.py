"""
Call handling and negotiation service
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from datetime import datetime
from src.models import Call, Carrier, Load, Negotiation
from src.schemas import CallStart, CallOutcome, Sentiment, NegotiationOffer
from src.fmcsa_service import FMCSAService
from src.load_service import LoadService
import logging

logger = logging.getLogger(__name__)


class CallHandlingService:
    """Service for handling carrier calls and negotiations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.fmcsa_service = FMCSAService()
        self.load_service = LoadService(db)
    
    async def start_call(self, call_data: CallStart) -> Tuple[bool, str, Optional[Call]]:
        """
        Start a new call with carrier verification
        
        Args:
            call_data: Call start data including MC number
            
        Returns:
            Tuple of (success, message, call_object)
        """
        try:
            # Verify carrier with FMCSA
            carrier_info = await self.fmcsa_service.verify_carrier(call_data.carrier_mc_number)
            
            if not carrier_info:
                return False, "Carrier not found in FMCSA database", None
            
            if not self.fmcsa_service.is_carrier_eligible(carrier_info):
                return False, f"Carrier {call_data.carrier_mc_number} is not eligible (Status: {carrier_info.operating_status})", None
            
            # Create or update carrier in database
            carrier = self._create_or_update_carrier(carrier_info)
            
            # Create call record
            call = Call(
                carrier_mc_number=call_data.carrier_mc_number,
                load_id=call_data.load_id,
                call_start_time=datetime.utcnow()
            )
            
            self.db.add(call)
            self.db.commit()
            self.db.refresh(call)
            
            logger.info(f"Call started with carrier {call_data.carrier_mc_number}")
            return True, f"Welcome {carrier_info.legal_name}! Your MC number has been verified.", call
            
        except Exception as e:
            logger.error(f"Error starting call: {str(e)}")
            return False, "System error occurred while verifying carrier", None
    
    def find_and_pitch_loads(self, call_id: int, carrier_preferences: Optional[dict] = None) -> List[Load]:
        """
        Find suitable loads and prepare pitch
        
        Args:
            call_id: Active call ID
            carrier_preferences: Optional carrier preferences for load matching
            
        Returns:
            List of suitable loads
        """
        call = self.db.query(Call).filter(Call.id == call_id).first()
        if not call:
            return []
        
        # Find suitable loads for the carrier
        suitable_loads = self.load_service.find_suitable_loads_for_carrier(
            carrier_mc_number=call.carrier_mc_number,
            preferred_origin=carrier_preferences.get('origin') if carrier_preferences else None,
            preferred_destination=carrier_preferences.get('destination') if carrier_preferences else None,
            equipment_types=carrier_preferences.get('equipment_types') if carrier_preferences else None,
            limit=5
        )
        
        return suitable_loads
    
    def handle_negotiation(self, call_id: str, carrier_offer: float, session_id: Optional[str] = None) -> Tuple[bool, str, bool]:
        """
        Handle negotiation round
        
        Args:
            call_id: Active call ID
            carrier_offer: Carrier's counter offer
            session_id: Optional session identifier for grouping negotiations
            
        Returns:
            Tuple of (accepted, response_message, should_transfer)
        """
        call = self.db.query(Call).filter(Call.id == call_id).first()
        if not call or not call.load_id:
            return False, "No active call or load found", False
        
        load = self.load_service.get_load(call.load_id)
        if not load:
            return False, "Load not found", False
        
        # Check negotiation rounds limit
        if call.negotiation_rounds >= 3:
            return False, "Maximum negotiation rounds reached. Let me transfer you to a sales representative.", True
        
        # Record negotiation round
        negotiation = Negotiation(
            call_id=call_id,
            session_id=session_id,
            round_number=call.negotiation_rounds + 1,
            carrier_offer=carrier_offer,
            timestamp=datetime.utcnow()
        )
        
        # Negotiation logic
        original_rate = load.loadboard_rate
        minimum_acceptable_rate = original_rate * 0.90  # Accept 10% below original rate
        ideal_rate = original_rate * 0.95  # Try to negotiate to 5% below original rate
        
        call.negotiation_rounds += 1
        
        if carrier_offer >= original_rate:
            # Carrier offered original rate or higher - accept immediately
            negotiation.system_response = "accepted"
            call.final_rate_agreed = carrier_offer
            call.outcome = CallOutcome.ACCEPTED
            
            self.db.add(negotiation)
            self.db.commit()
            
            return True, f"Excellent! We accept your offer of ${carrier_offer:.2f}. Let me transfer you to complete the booking.", True
        
        elif carrier_offer >= minimum_acceptable_rate:
            # Carrier offer is within acceptable range
            if call.negotiation_rounds == 1:
                # First round - try to negotiate up slightly
                counter_offer = min(ideal_rate, carrier_offer * 1.03)
                negotiation.system_response = f"counter_offer_{counter_offer}"
                
                self.db.add(negotiation)
                self.db.commit()
                
                return False, f"I appreciate your offer of ${carrier_offer:.2f}. Given the urgency and mileage, could we meet at ${counter_offer:.2f}?", False
            else:
                # Later rounds - be more flexible
                negotiation.system_response = "accepted"
                call.final_rate_agreed = carrier_offer
                call.outcome = CallOutcome.ACCEPTED
                
                self.db.add(negotiation)
                self.db.commit()
                
                return True, f"I can work with ${carrier_offer:.2f}. Let me get you connected with our dispatch team to finalize the details.", True
        
        else:
            # Offer too low
            if call.negotiation_rounds < 3:
                counter_offer = max(minimum_acceptable_rate, original_rate * 0.93)
                negotiation.system_response = f"counter_offer_{counter_offer}"
                
                self.db.add(negotiation)
                self.db.commit()
                
                return False, f"I understand your position at ${carrier_offer:.2f}, but that's quite a bit below our rate. How about ${counter_offer:.2f}? This load has great backhaul opportunities.", False
            else:
                # Final round - transfer to human
                negotiation.system_response = "transfer_to_human"
                
                self.db.add(negotiation)
                self.db.commit()
                
                return False, "I understand we're not quite aligned on rate. Let me connect you with our sales manager who may have more flexibility.", True
    
    def end_call(self, call_id: int, outcome: CallOutcome, sentiment: Sentiment, notes: Optional[str] = None):
        """End a call and update records"""
        call = self.db.query(Call).filter(Call.id == call_id).first()
        if call:
            call.call_end_time = datetime.utcnow()
            call.call_duration = int((call.call_end_time - call.call_start_time).total_seconds())
            call.outcome = outcome
            call.sentiment = sentiment
            if notes:
                call.notes = notes
            
            # If load was accepted, book it
            if outcome == CallOutcome.ACCEPTED and call.final_rate_agreed and call.load_id:
                self.load_service.book_load(
                    call.load_id,
                    call.carrier_mc_number,
                    call.final_rate_agreed
                )
            
            self.db.commit()
            logger.info(f"Call {call_id} ended with outcome: {outcome}")
    
    def _create_or_update_carrier(self, carrier_info) -> Carrier:
        """Create or update carrier in database"""
        carrier = self.db.query(Carrier).filter(
            Carrier.mc_number == carrier_info.mc_number
        ).first()
        
        if carrier:
            # Update existing carrier
            carrier.company_name = carrier_info.legal_name
            carrier.status = carrier_info.operating_status
            carrier.phone = carrier_info.phone
            carrier.address = carrier_info.physical_address
            carrier.is_verified = True
            carrier.updated_at = datetime.utcnow()
        else:
            # Create new carrier
            carrier = Carrier(
                mc_number=carrier_info.mc_number,
                company_name=carrier_info.legal_name,
                status=carrier_info.operating_status,
                phone=carrier_info.phone,
                address=carrier_info.physical_address,
                is_verified=True
            )
            self.db.add(carrier)
        
        self.db.commit()
        self.db.refresh(carrier)
        return carrier
