# Quick Setup Instructions

## 🚀 EASIEST WAY: One-Click Setup & Run

**Just double-click:** `START.bat` or `RUN_EVERYTHING.bat`

This single file will:
- ✅ Check Python version
- ✅ Install all dependencies automatically (if needed)
- ✅ Initialize database
- ✅ Start the backend server
- ✅ Start chat interface
- ✅ Start dashboard

**That's it!** No manual steps needed.

**Note:** Pehle ek baar `INSTALL_EVERYTHING.bat` run karo dependencies ke liye.

---

## Alternative: Manual Setup

## Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python scripts/setup.py
```

### 3. (Optional) Seed Sample Data

```bash
python scripts/seed_data.py
```

### 4. Start Backend API

In Terminal 1:
```bash
# From project root
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://localhost:8000
API Docs: http://localhost:8000/docs

### 5. Start Chat Interface

In Terminal 2:
```bash
streamlit run frontend/chat_interface.py
```

The chat interface will open at: http://localhost:8501

### 6. Start Analytics Dashboard (Optional)

In Terminal 3:
```bash
streamlit run frontend/dashboard.py
```

The dashboard will open at: http://localhost:8502

## Using Docker (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Testing the System

1. **Test Chat Interface**: 
   - Open http://localhost:8501
   - Type messages like "I need help with my order" or "I want a refund"
   - Watch agent responses and escalation behavior

2. **Test Dashboard**:
   - Open http://localhost:8502
   - View analytics and metrics
   - Refresh data to see updates

3. **Test API Directly**:
   - Open http://localhost:8000/docs
   - Use Swagger UI to test endpoints
   - Try POST /api/v1/chat with sample messages

## Troubleshooting

**Port Already in Use**:
- Backend API: Change port in `backend/main.py` or use `--port` flag
- Streamlit: Use `--server.port` flag to specify different port

**Database Errors**:
- Ensure database directory exists: `mkdir -p database`
- Run setup script: `python scripts/setup.py`

**Import Errors**:
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

## Common Issues

**Backend won't start**:
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check Python version compatibility

**Frontend can't connect to backend**:
- Ensure backend is running on port 8000
- Check API_BASE_URL in frontend files
- Check firewall/network settings

**No data in dashboard**:
- Seed sample data: `python scripts/seed_data.py`
- Have conversations in chat interface first
- Check if database is populated
