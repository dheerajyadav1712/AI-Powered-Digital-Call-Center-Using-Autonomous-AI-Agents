"""
Setup script for AI Digital Call Center.
Initializes database and creates necessary directories.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.core.database import init_db
from backend.app.core.config import settings


def main():
    """Main setup function."""
    print("=" * 50)
    print("AI Digital Call Center - Setup")
    print("=" * 50)
    
    # Create database directory
    db_dir = Path(settings.DATABASE_DIR)
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created database directory: {db_dir}")
    
    # Initialize database
    print("\nInitializing database...")
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {str(e)}")
        return
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run backend: uvicorn backend.main:app --reload")
    print("3. Run chat interface: streamlit run frontend/chat_interface.py")
    print("4. Run dashboard: streamlit run frontend/dashboard.py")
    print("5. (Optional) Seed sample data: python scripts/seed_data.py")


if __name__ == "__main__":
    main()


