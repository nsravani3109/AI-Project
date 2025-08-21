"""
Data initialization script to populate the database with sample data
"""
import json
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine
from src.models import Base, Load, Carrier
from src.schemas import LoadCreate


def load_sample_data():
    """Load sample data into the database"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Load).count() > 0:
            print("Sample data already exists. Skipping initialization.")
            return
        
        # Load sample loads
        with open('data/sample_loads.json', 'r') as f:
            loads_data = json.load(f)
        
        for load_data in loads_data:
            # Convert datetime strings to datetime objects
            load_data['pickup_datetime'] = datetime.fromisoformat(
                load_data['pickup_datetime'].replace('Z', '+00:00')
            )
            load_data['delivery_datetime'] = datetime.fromisoformat(
                load_data['delivery_datetime'].replace('Z', '+00:00')
            )
            
            load = Load(**load_data)
            db.add(load)
        
        # Create sample carriers (these would normally be created via FMCSA verification)
        sample_carriers = [
            {
                "mc_number": "MC-123456",
                "company_name": "ABC Trucking LLC",
                "status": "ACTIVE",
                "phone": "(555) 123-4567",
                "address": "123 Main St, Springfield, IL 62701",
                "is_verified": True
            },
            {
                "mc_number": "MC-789012",
                "company_name": "XYZ Transport Inc",
                "status": "ACTIVE",
                "phone": "(555) 987-6543",
                "address": "456 Oak Ave, Chicago, IL 60601",
                "is_verified": True
            },
            {
                "mc_number": "MC-345678",
                "company_name": "Reliable Freight Solutions",
                "status": "OUT-OF-SERVICE",
                "phone": "(555) 456-7890",
                "address": "789 Pine St, Detroit, MI 48201",
                "is_verified": True
            }
        ]
        
        for carrier_data in sample_carriers:
            carrier = Carrier(**carrier_data)
            db.add(carrier)
        
        db.commit()
        print("Sample data loaded successfully!")
        print(f"Loaded {len(loads_data)} loads and {len(sample_carriers)} carriers.")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    load_sample_data()
