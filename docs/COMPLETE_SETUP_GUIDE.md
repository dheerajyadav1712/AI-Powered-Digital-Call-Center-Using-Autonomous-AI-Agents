# 📚 Complete Setup & Usage Guide - AI Digital Call Center

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [How to Use Chat Interface](#how-to-use-chat-interface)
5. [How to Use Dashboard](#how-to-use-dashboard)
6. [Ticket System Workflow](#ticket-system-workflow)
7. [Agent Behavior & Escalation](#agent-behavior--escalation)
8. [Troubleshooting](#troubleshooting)

---

## 1. System Requirements

### Software Requirements:
- **Python 3.10 or higher** (3.11+ recommended)
- **pip** (Python package manager - comes with Python)
- **Internet Connection** (for initial installation only)
- **Web Browser** (Chrome, Firefox, Edge, Safari)

### Hardware Requirements:
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** ~500 MB free space
- **Processor:** Any modern processor (Intel/AMD)

---

## 2. Installation Steps

### Step 1: Install Python

**Windows:**
1. Download Python from: https://www.python.org/downloads/
2. Run installer
3. ✅ **CRITICAL:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open Command Prompt → `python --version`

**Mac:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

### Step 2: Install Dependencies

**Automatic (Recommended):**
```bash
# Double-click: INSTALL_EVERYTHING.bat
# OR run:
python -m pip install -r requirements.txt
```

**Manual:**
```bash
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn streamlit sqlalchemy plotly requests pydantic
```

### Step 3: Verify Installation

```bash
python -c "import fastapi, streamlit; print('✅ Installation successful!')"
```

---

## 3. Running the Application

### Method 1: One-Click Start (Easiest)

**Just double-click:** `START.bat` or `RUN_EVERYTHING.bat`

This automatically:
- ✅ Checks dependencies
- ✅ Initializes database
- ✅ Starts Backend API (port 8000)
- ✅ Starts Chat Interface (port 8501)
- ✅ Starts Dashboard (port 8502)

### Method 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Chat Interface:**
```bash
streamlit run frontend/chat_interface.py --server.port 8501
```

**Terminal 3 - Dashboard (Optional):**
```bash
streamlit run frontend/dashboard.py --server.port 8502
```

---

## 4. How to Use Chat Interface

### Accessing Chat Interface

1. Start the application (see Section 3)
2. Open browser: http://localhost:8501
3. Chat interface will open

### Chat Features

**Conversation Flow:**
1. Type your message in the input box
2. Click "Send" or press Enter
3. AI agent responds immediately
4. View agent details (confidence, intent, sentiment) in expandable section

### Example Conversations

**Greeting:**
```
You: Hi
Agent: Hello! 👋 Thank you for contacting our support team. How can I help you today?
```

**Order Inquiry:**
```
You: I need help with my order
Agent: I'd be happy to help you with your order. Could you provide your order number?
```

**Complex Query (Escalation):**
```
You: I'm having a critical security issue
Agent: This requires specialized attention. Creating a ticket for IS Security team...
Ticket #TKT-20240115-001 created!
```

### Chat Interface Elements

- **Message Input:** Type your message at the bottom
- **Chat History:** All messages displayed in conversation format
- **Agent Details:** Click expander to see confidence, intent, sentiment
- **New Conversation:** Click sidebar button to start fresh

---

## 5. How to Use Dashboard

### Accessing Dashboard

1. Ensure backend is running
2. Open browser: http://localhost:8502
3. Dashboard will load with real-time metrics

### Dashboard Features

**Key Metrics:**
- Total Conversations
- Resolved Conversations
- Escalated Conversations
- Average CSAT Score
- Average Agent Confidence

**Visualizations:**
- Conversations by Agent Type (Bar Chart)
- Conversations by Intent (Pie Chart)
- Conversations by Sentiment (Bar Chart)

**Performance Metrics:**
- Average Resolution Time
- Escalation Rate
- Resolution Rate

### Refreshing Data

Click "🔄 Refresh Data" button to update metrics

---

## 6. Ticket System Workflow

### When Tickets are Created

Tickets are automatically suggested when:
- Agent confidence is too low (< 60%)
- Query requires specialized team attention
- User explicitly requests ticket
- Complex technical issues that need tracking

### Ticket Categories

1. **GHD** (Global Help Desk)
   - General IT support
   - Account issues
   - Access requests

2. **Internal IT**
   - Infrastructure issues
   - System maintenance
   - Server problems

3. **IS Security**
   - Security incidents
   - Access violations
   - Data breaches
   - Security configurations

4. **Proxy**
   - Network proxy issues
   - VPN problems
   - Connectivity issues

5. **Configuration and Queries**
   - System configurations
   - Setting changes
   - Technical queries
   - Documentation requests

### Ticket Creation Process

**Step 1: Agent Identifies Need**
```
Agent: "This issue requires a ticket for tracking. Let me create one for you."
```

**Step 2: Category Selection**
```
Agent: "Which category does your issue fall under?
- GHD
- Internal IT
- IS Security
- Proxy
- Configuration and Queries"
```

**Step 3: Problem Description**
```
Agent: "Please provide a detailed description of your problem."
You: [Describe your issue]
```

**Step 4: Ticket Number Assignment**
```
Agent: "Thank you! Your ticket has been created.
Ticket Number: TKT-20240115-001
Category: IS Security
Status: Open

You can track this ticket using the ticket number above."
```

**Step 5: Ticket Tracking**
- Ticket number is stored in database
- Can be tracked via dashboard
- Status updates available

### Ticket Format

**Format:** `TKT-YYYYMMDD-XXX`
- Example: `TKT-20240115-001`
- Date-based tracking
- Sequential number per day

### Viewing Tickets

**Via Dashboard:**
- Open dashboard: http://localhost:8502
- Check "Tickets" section
- Filter by category, status, date

**Via API:**
```bash
GET http://localhost:8000/api/v1/tickets
GET http://localhost:8000/api/v1/tickets/{ticket_number}
```

---

## 7. Agent Behavior & Escalation

### Agent Hierarchy

**1. Primary Agent (First Line)**
- Handles routine queries
- Confidence threshold: 70%
- Handles: greetings, basic questions, simple issues

**2. Supervisor Agent (Second Line)**
- Handles complex queries
- Confidence threshold: 85%
- Handles: escalated issues, complex problems

**3. Escalation Agent (Third Line)**
- Manages ticket creation
- Handles: human handoff, ticket generation
- Creates tickets when needed

### Escalation Triggers

**Automatic Escalation:**
- Low confidence (< 60%)
- Security-related issues
- Critical system problems
- Explicit ticket request

**Manual Escalation:**
- User requests human agent
- User mentions "ticket" or "create ticket"
- Multiple failed resolution attempts

### Response Quality

**All agents provide:**
- Natural, conversational responses
- Context-aware answers
- Helpful suggestions
- Clear next steps

**Response Time:**
- Instant responses (< 1 second)
- Real-time processing
- No delays or timeouts

---

## 8. Troubleshooting

### Issue: Chat Interface Not Loading

**Solution:**
1. Check if backend is running: http://localhost:8000/health
2. Check browser console for errors (F12)
3. Restart both backend and frontend

### Issue: No Response from Agent

**Solution:**
1. Check backend logs for errors
2. Verify API connection: http://localhost:8000/api/v1/health
3. Check network connectivity

### Issue: Dashboard Shows No Data

**Solution:**
1. Ensure backend has processed some conversations
2. Seed sample data: `python scripts/seed_data.py`
3. Check database file exists: `database/call_center.db`

### Issue: Ticket Not Created

**Solution:**
1. Check if issue matches escalation criteria
2. Verify ticket system is enabled
3. Check backend logs for errors

### Issue: Port Already in Use

**Solution:**
1. Close other applications using ports 8000, 8501, 8502
2. Or change ports in configuration files
3. Use `netstat -ano | findstr :8000` to find processes

---

## Quick Reference

### URLs:
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Chat Interface:** http://localhost:8501
- **Dashboard:** http://localhost:8502

### Key Commands:
```bash
# Start everything
START.bat

# Install dependencies
INSTALL_EVERYTHING.bat

# Seed sample data
python scripts/seed_data.py

# Check backend health
curl http://localhost:8000/api/v1/health
```

### Ticket Categories:
1. GHD
2. Internal IT
3. IS Security
4. Proxy
5. Configuration and Queries

---

## Support

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Check error logs in backend terminal
4. Verify all requirements are met

---

**Last Updated:** 2024-01-15
**Version:** 1.0.0


