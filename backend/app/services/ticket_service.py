"""
Ticket service for creating and managing support tickets.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from app.models.database_models import Ticket, Conversation


class TicketService:
    """
    Service for managing support tickets.
    """
    
    TICKET_CATEGORIES = [
        "GHD",
        "Internal IT",
        "IS Security",
        "Proxy",
        "Configuration and Queries"
    ]
    
    def generate_ticket_number(self) -> str:
        """
        Generate unique ticket number.
        Format: TKT-YYYYMMDD-XXX
        """
        date_str = datetime.now().strftime("%Y%m%d")
        
        # In production, you'd query database for count of tickets today
        # For now, use UUID for uniqueness
        unique_part = str(uuid.uuid4())[:3].upper()
        
        return f"TKT-{date_str}-{unique_part}"
    
    def create_ticket(
        self,
        category: str,
        description: str,
        conversation_id: Optional[int] = None,
        customer_id: Optional[str] = None,
        title: Optional[str] = None,
        priority: str = "medium",
        db: Optional[Session] = None
    ) -> Dict:
        """
        Create a new support ticket.
        
        Args:
            category: Ticket category
            description: Problem description
            conversation_id: Associated conversation ID
            customer_id: Customer identifier
            title: Ticket title (optional)
            priority: Ticket priority
            db: Database session
            
        Returns:
            Dictionary with ticket information
        """
        # Generate ticket number
        ticket_number = self.generate_ticket_number()
        
        # Create ticket object
        ticket = Ticket(
            ticket_number=ticket_number,
            conversation_id=conversation_id,
            customer_id=customer_id,
            category=category,
            title=title or f"Issue in {category}",
            description=description,
            status="open",
            priority=priority,
            created_at=datetime.now()
        )
        
        # Save to database if session provided
        if db:
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
        
        return {
            "ticket_number": ticket_number,
            "category": category,
            "title": ticket.title,
            "description": description,
            "status": "open",
            "priority": priority,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else datetime.now().isoformat()
        }
    
    def get_ticket(self, ticket_number: str, db: Session) -> Optional[Ticket]:
        """
        Get ticket by ticket number.
        
        Args:
            ticket_number: Ticket number
            db: Database session
            
        Returns:
            Ticket object or None
        """
        return db.query(Ticket).filter(
            Ticket.ticket_number == ticket_number
        ).first()
    
    def get_tickets_by_conversation(self, conversation_id: int, db: Session) -> list:
        """
        Get all tickets for a conversation.
        
        Args:
            conversation_id: Conversation ID
            db: Database session
            
        Returns:
            List of ticket objects
        """
        return db.query(Ticket).filter(
            Ticket.conversation_id == conversation_id
        ).all()


ticket_service = TicketService()


