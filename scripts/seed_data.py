"""
Script to seed sample data for demonstration purposes.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.core.database import SessionLocal, init_db
from backend.app.models.database_models import Conversation, Message, Feedback, AgentMetric
from backend.app.agents.primary_agent import primary_agent
from backend.app.agents.supervisor_agent import supervisor_agent


def seed_conversations(db, num_conversations=20):
    """Seed sample conversations."""
    print(f"Seeding {num_conversations} sample conversations...")
    
    sample_messages = [
        "I need help with my order",
        "When will my package arrive?",
        "I want to return this product",
        "My account is not working",
        "I'm having trouble with billing",
        "Thank you for the great service!",
        "I have a complaint about my purchase",
        "Can you help me track my shipment?",
        "I need to cancel my subscription",
        "There's an issue with my payment",
        "I'm very satisfied with your service",
        "How do I reset my password?",
        "I want to speak to a manager",
        "The product I received is broken",
        "I love your product!",
        "Can you explain the refund policy?",
        "I need technical support",
        "This is terrible, I want a refund",
        "Hello, I need assistance",
        "Thank you so much for helping me"
    ]
    
    intents = [
        "order_inquiry", "tracking_inquiry", "refund_request",
        "account_management", "billing_inquiry", "praise",
        "complaint", "technical_support", "greeting"
    ]
    
    sentiments = ["positive", "neutral", "negative"]
    
    for i in range(num_conversations):
        # Create conversation
        conversation = Conversation(
            session_id=f"session_{i+1}_{random.randint(1000, 9999)}",
            customer_id=f"customer_{random.randint(100, 999)}",
            channel="chat",
            status=random.choice(["active", "resolved", "escalated"]),
            started_at=datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23)),
            primary_agent_handled=True,
            supervisor_agent_handled=random.choice([True, False]),
            human_agent_handled=random.choice([True, False])
        )
        
        # Set end time if resolved
        if conversation.status == "resolved":
            conversation.ended_at = conversation.started_at + timedelta(minutes=random.randint(5, 30))
            conversation.resolved_at = conversation.ended_at
            conversation.resolution_time_seconds = int(
                (conversation.ended_at - conversation.started_at).total_seconds()
            )
        elif conversation.status == "escalated":
            conversation.escalated_at = conversation.started_at + timedelta(minutes=random.randint(2, 10))
            conversation.ended_at = conversation.escalated_at + timedelta(minutes=random.randint(10, 45))
            conversation.resolution_time_seconds = int(
                (conversation.ended_at - conversation.started_at).total_seconds()
            )
        
        db.add(conversation)
        db.flush()
        
        # Add customer message
        customer_msg_text = random.choice(sample_messages)
        customer_message = Message(
            conversation_id=conversation.id,
            role="customer",
            content=customer_msg_text,
            intent=random.choice(intents),
            sentiment_score=random.uniform(-0.8, 0.8),
            sentiment_label=random.choice(sentiments),
            confidence_score=random.uniform(0.6, 0.95),
            created_at=conversation.started_at
        )
        db.add(customer_message)
        
        # Add agent response
        agent_type = "primary"
        if conversation.supervisor_agent_handled:
            agent_type = "supervisor"
        elif conversation.human_agent_handled:
            agent_type = "human_agent"
        
        agent_message = Message(
            conversation_id=conversation.id,
            role=agent_type,
            content=f"Thank you for contacting us. {random.choice(['I can help with that.', 'Let me assist you.', 'I understand your concern.'])}",
            intent=random.choice(intents),
            sentiment_score=random.uniform(0.3, 0.9),
            sentiment_label="positive",
            confidence_score=random.uniform(0.7, 0.95),
            created_at=conversation.started_at + timedelta(seconds=random.randint(5, 30))
        )
        db.add(agent_message)
        
        # Add feedback if resolved
        if conversation.status == "resolved" and random.choice([True, False]):
            feedback = Feedback(
                conversation_id=conversation.id,
                csat_score=random.randint(3, 5),
                feedback_text=random.choice([
                    "Great service!",
                    "Very helpful agent",
                    "Issue resolved quickly",
                    "Satisfied with the response",
                    None
                ]),
                submitted_at=conversation.ended_at + timedelta(minutes=random.randint(1, 10))
            )
            db.add(feedback)
        
        if (i + 1) % 5 == 0:
            print(f"  Created {i + 1}/{num_conversations} conversations")
    
    db.commit()
    print(f"✓ Seeded {num_conversations} conversations")


def seed_agent_metrics(db):
    """Seed sample agent metrics."""
    print("Seeding agent metrics...")
    
    agent_types = ["primary", "supervisor", "escalation", "human"]
    
    for agent_type in agent_types:
        metric = AgentMetric(
            agent_type=agent_type,
            date=datetime.now(),
            conversations_handled=random.randint(50, 200),
            average_confidence=random.uniform(0.75, 0.95),
            average_response_time_seconds=random.uniform(5, 30),
            escalation_count=random.randint(0, 20) if agent_type != "human" else 0,
            resolution_rate=random.uniform(0.70, 0.95)
        )
        db.add(metric)
    
    db.commit()
    print("✓ Seeded agent metrics")


def main():
    """Main seeding function."""
    print("=" * 50)
    print("AI Digital Call Center - Sample Data Seeding")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("\nClearing existing data...")
        db.query(Feedback).delete()
        db.query(Message).delete()
        db.query(Conversation).delete()
        db.query(AgentMetric).delete()
        db.commit()
        print("✓ Cleared existing data")
        
        # Seed data
        print("\nSeeding data...")
        seed_conversations(db, num_conversations=30)
        seed_agent_metrics(db)
        
        print("\n" + "=" * 50)
        print("✓ Sample data seeding completed successfully!")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n✗ Error seeding data: {str(e)}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()


