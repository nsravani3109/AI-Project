"""
HappyRobot platform integration service
"""
import requests
import logging
from typing import Dict, Any, Optional
from config.settings import settings

logger = logging.getLogger(__name__)


class HappyRobotService:
    """Service for integrating with HappyRobot platform"""
    
    def __init__(self):
        self.base_url = settings.happyrobot_base_url
        self.api_key = settings.happyrobot_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_inbound_agent(self, agent_config: Dict[str, Any]) -> Optional[Dict]:
        """
        Create an inbound agent configuration
        
        Args:
            agent_config: Configuration for the inbound agent
            
        Returns:
            Agent configuration if successful, None otherwise
        """
        try:
            # This is a mock implementation
            # In reality, you would call the HappyRobot API to create an agent
            
            default_config = {
                "agent_id": "inbound-carrier-sales-agent",
                "name": "Inbound Carrier Sales Agent",
                "description": "AI agent for handling inbound carrier calls and load booking",
                "capabilities": [
                    "carrier_verification",
                    "load_matching",
                    "price_negotiation",
                    "call_transfer"
                ],
                "webhook_url": f"http://localhost:{settings.port}/api/webhook/happyrobot",
                "voice_config": {
                    "voice": "professional_female",
                    "speed": "normal",
                    "language": "en-US"
                },
                "conversation_flow": {
                    "greeting": "Hello! Thank you for calling. I'm your AI assistant for load booking. May I have your MC number to get started?",
                    "verification_success": "Great! I've verified your carrier information. Let me find some suitable loads for you.",
                    "verification_failure": "I'm sorry, but I couldn't verify your MC number. Please ensure it's correct or contact our customer service.",
                    "no_loads": "I don't have any loads that match your requirements right now, but I can transfer you to our dispatch team to check for upcoming opportunities.",
                    "negotiation_intro": "I can see you're interested in this load. The posted rate is ${{rate}}. What rate would work for you?",
                    "transfer_message": "Let me connect you with one of our experienced sales representatives who can finalize the booking details."
                }
            }
            
            # Merge with provided config
            merged_config = {**default_config, **agent_config}
            
            logger.info(f"Created inbound agent configuration: {merged_config['agent_id']}")
            return merged_config
            
        except Exception as e:
            logger.error(f"Error creating inbound agent: {str(e)}")
            return None
    
    def configure_webhooks(self, webhook_config: Dict[str, Any]) -> bool:
        """
        Configure webhooks for receiving call events
        
        Args:
            webhook_config: Webhook configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Mock webhook configuration
            # In reality, this would configure HappyRobot to send events to our API
            
            logger.info("Webhook configuration completed")
            return True
            
        except Exception as e:
            logger.error(f"Error configuring webhooks: {str(e)}")
            return False
    
    def get_call_transcript(self, call_id: str) -> Optional[str]:
        """
        Retrieve call transcript from HappyRobot
        
        Args:
            call_id: HappyRobot call ID
            
        Returns:
            Call transcript if available, None otherwise
        """
        try:
            # Mock implementation
            # In reality, this would fetch the actual transcript from HappyRobot
            
            return f"Mock transcript for call {call_id}"
            
        except Exception as e:
            logger.error(f"Error fetching call transcript: {str(e)}")
            return None
    
    def trigger_call_transfer(self, call_id: str, transfer_number: str) -> bool:
        """
        Trigger call transfer to human representative
        
        Args:
            call_id: Active call ID
            transfer_number: Phone number to transfer to
            
        Returns:
            True if transfer initiated successfully, False otherwise
        """
        try:
            # Mock implementation
            # In reality, this would trigger an actual call transfer via HappyRobot API
            
            logger.info(f"Call {call_id} transfer initiated to {transfer_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error initiating call transfer: {str(e)}")
            return False
    
    def update_agent_script(self, agent_id: str, script_updates: Dict[str, str]) -> bool:
        """
        Update agent conversation script
        
        Args:
            agent_id: Agent identifier
            script_updates: Script updates to apply
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Mock implementation
            # In reality, this would update the agent's conversation flow via API
            
            logger.info(f"Agent {agent_id} script updated")
            return True
            
        except Exception as e:
            logger.error(f"Error updating agent script: {str(e)}")
            return False


def initialize_happyrobot_agent():
    """Initialize the HappyRobot inbound agent"""
    service = HappyRobotService()
    
    agent_config = {
        "specialized_prompts": {
            "load_pitch": "I have a great load opportunity for you: {{origin}} to {{destination}}, picking up {{pickup_date}} and delivering {{delivery_date}}. The rate is ${{rate}} for {{miles}} miles. The equipment needed is {{equipment_type}}. Are you interested in hearing more details?",
            "negotiation_response": "I understand your position. Let me see what I can do. The original rate was ${{original_rate}}. Given the mileage and delivery requirements, how about we meet at ${{counter_offer}}?",
            "booking_confirmation": "Excellent! I'm booking load {{load_id}} for you at ${{agreed_rate}}. Let me transfer you to our dispatch team to get all the pickup and delivery details finalized."
        }
    }
    
    # Create agent configuration
    config = service.create_inbound_agent(agent_config)
    
    # Configure webhooks
    webhook_config = {
        "events": ["call_started", "call_ended", "transcript_ready"],
        "url": f"http://localhost:{settings.port}/api/webhook/happyrobot",
        "secret": settings.secret_key
    }
    
    service.configure_webhooks(webhook_config)
    
    return config


if __name__ == "__main__":
    # Initialize the agent when running this script directly
    config = initialize_happyrobot_agent()
    print("HappyRobot agent initialized:", config)
