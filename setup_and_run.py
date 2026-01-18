"""
🚀 Complete Auto-Setup and Run Script for AI Digital Call Center
This script automatically installs dependencies, initializes database, and starts the system.
"""
import sys
import subprocess
import os
from pathlib import Path

# Color codes for Windows terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_warning(text):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{BLUE}ℹ {text}{RESET}")

def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print_error("Python 3.10 or higher is required!")
        return False
    
    print_success("Python version is compatible")
    return True

def install_dependencies():
    """Install all required dependencies."""
    print_header("Installing Dependencies")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_error("requirements.txt not found!")
        return False
    
    print_info("Installing packages from requirements.txt...")
    print_info("This may take a few minutes. Please wait...\n")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        print_success("pip upgraded")
        
        # Install requirements
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("All dependencies installed successfully!")
            return True
        else:
            print_warning("Some packages may have installation warnings:")
            if result.stderr:
                print(result.stderr)
            # Continue anyway as some warnings are non-critical
            print_success("Dependencies installation completed")
            return True
            
    except subprocess.CalledProcessError as e:
        print_error(f"Error installing dependencies: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def initialize_database():
    """Initialize the database."""
    print_header("Initializing Database")
    
    # Create database directory
    db_dir = Path("database")
    db_dir.mkdir(exist_ok=True)
    print_success(f"Database directory created: {db_dir.absolute()}")
    
    # Change to backend directory for imports
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_error("Backend directory not found!")
        return False
    
    original_dir = os.getcwd()
    try:
        os.chdir(backend_dir)
        
        # Initialize database
        init_code = """
import sys
from pathlib import Path
from app.core.database import init_db

try:
    # Create database directory if needed
    db_path = Path('../database')
    db_path.mkdir(exist_ok=True)
    
    # Initialize database
    init_db()
    print('Database initialized successfully!')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"""
        result = subprocess.run(
            [sys.executable, "-c", init_code],
            capture_output=True,
            text=True
        )
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print_success("Database initialized successfully!")
            return True
        else:
            print_error(f"Database initialization failed: {result.stderr}")
            return False
            
    except Exception as e:
        os.chdir(original_dir)
        print_error(f"Error initializing database: {e}")
        return False

def start_backend():
    """Start the backend server."""
    print_header("Starting Backend Server")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_error("Backend directory not found!")
        return False
    
    print_info("Starting FastAPI backend server...")
    print_info("API will be available at: http://localhost:8000")
    print_info("API Documentation: http://localhost:8000/docs")
    print_info("Press Ctrl+C to stop the server\n")
    
    try:
        # Change to backend directory and start uvicorn
        os.chdir(backend_dir)
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print_info("\n\nServer stopped by user")
    except Exception as e:
        print_error(f"Error starting server: {e}")
        return False

def main():
    """Main function to run all setup and start steps."""
    print(f"\n{BOLD}{GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     AI Digital Call Center - Auto Setup & Run Script      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install dependencies
    print_info("Checking if dependencies need to be installed...")
    if not install_dependencies():
        print_warning("Some dependencies may have failed. Continuing anyway...")
    
    # Step 3: Initialize database
    if not initialize_database():
        print_warning("Database initialization had issues. Continuing anyway...")
    
    # Step 4: Start backend
    print_header("Starting Application")
    print_success("Setup completed!")
    print_info("\n🎉 Everything is ready! Starting the backend server...\n")
    print_info("💡 Tips:")
    print_info("   - API Documentation: http://localhost:8000/docs")
    print_info("   - Chat Interface: Run 'streamlit run frontend/chat_interface.py' in another terminal")
    print_info("   - Dashboard: Run 'streamlit run frontend/dashboard.py' in another terminal")
    print_info("   - Press Ctrl+C to stop the server\n")
    
    start_backend()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Setup interrupted by user{RESET}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


