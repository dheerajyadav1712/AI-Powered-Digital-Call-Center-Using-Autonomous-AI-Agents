# 📖 Step-by-Step Complete Guide - AI Digital Call Center

## 🎯 Quick Navigation
- [Installation](#installation)
- [Running the System](#running-the-system)
- [Using Chat Interface](#using-chat-interface)
- [Ticket System](#ticket-system)
- [Dashboard Usage](#dashboard-usage)

---

## 1️⃣ Installation

### Step 1: Install Python
1. Download from: https://www.python.org/downloads/
2. Install with "Add Python to PATH" checked
3. Verify: `python --version` (should show 3.10+)

### Step 2: Install Dependencies
**Double-click:** `INSTALL_EVERYTHING.bat`

OR manually:
```bash
python -m pip install -r requirements.txt
```

### Step 3: Verify
```bash
python -c "import fastapi, streamlit; print('✅ Ready!')"
```

---

## 2️⃣ Running the System

### One-Click Start
**Double-click:** `START.bat` or `RUN_EVERYTHING.bat`

This starts:
- ✅ Backend API (http://localhost:8000)
- ✅ Chat Interface (http://localhost:8501)
- ✅ Dashboard (http://localhost:8502)

---

## 3️⃣ Using Chat Interface

### Step 1: Open Chat
- URL: http://localhost:8501
- Type message in input box
- Press Enter or click Send

### Step 2: Agent Responses
- **Greetings:** "Hi", "Hello" → Friendly welcome
- **Questions:** Ask anything → Relevant response
- **Complex Issues:** Automatic escalation to ticket

### Step 3: View Agent Details
- Click "Agent Details" expander
- See confidence, intent, sentiment

---

## 4️⃣ Ticket System

### When Tickets are Created

Tickets are automatically suggested when:
- ❌ Agent cannot resolve (low confidence)
- 🔒 Security issues detected
- ⚙️ Technical problems requiring tracking
- 📋 User requests ticket

### Ticket Categories

1. **GHD** - General Help Desk
2. **Internal IT** - Infrastructure/Systems
3. **IS Security** - Security incidents
4. **Proxy** - Network/Connectivity
5. **Configuration and Queries** - Setup/Config

### Ticket Creation Flow

**Example Conversation:**

```
User: I have a security issue with my account
Agent: This requires specialized attention. I'll create a ticket for IS Security team.
       Please provide a detailed description of your problem.

User: [Provides description]
Agent: Thank you! Ticket created:
       📋 Ticket Number: TKT-20240115-001
       Category: IS Security
       Status: Open
       
       Ticket No: TKT-20240115-001
       You can track this ticket using the number above.
```

### Ticket Format
- Format: `TKT-YYYYMMDD-XXX`
- Example: `TKT-20240115-001`
- Trackable via dashboard

---

## 5️⃣ Dashboard Usage

### Access Dashboard
- URL: http://localhost:8502

### View Metrics
- **KPIs:** Total conversations, CSAT, resolution rate
- **Charts:** Agent performance, intent distribution
- **Tickets:** Ticket status and tracking

### Refresh Data
- Click "🔄 Refresh Data" button

---

## 💡 Common Use Cases

### Use Case 1: Simple Query
```
User: Hi
Agent: Hello! 👋 How can I help you?
```

### Use Case 2: Order Inquiry
```
User: I need help with my order
Agent: I'd be happy to help. Please provide your order number.
```

### Use Case 3: Security Issue (Ticket)
```
User: My account was hacked
Agent: This is a security issue. Creating ticket for IS Security...
       Please describe the problem.

User: [Description]
Agent: Ticket TKT-20240115-001 created! You can track it.
```

### Use Case 4: Technical Problem (Ticket)
```
User: I can't access the proxy server
Agent: This requires network team. Creating ticket for Proxy...
       Please describe your issue.

User: [Description]
Agent: Ticket TKT-20240115-002 created! Status: Open
```

---

## 🔧 Troubleshooting

### Problem: Chat not responding
**Solution:** Check backend is running: http://localhost:8000/health

### Problem: No ticket created
**Solution:** Ensure issue matches escalation criteria

### Problem: Dashboard empty
**Solution:** Run `python scripts/seed_data.py` for sample data

---

## 📝 Quick Commands

```bash
# Install dependencies
INSTALL_EVERYTHING.bat

# Start everything
START.bat

# Check backend
curl http://localhost:8000/api/v1/health

# Seed sample data
python scripts/seed_data.py
```

---

**Last Updated:** 2024-01-15


