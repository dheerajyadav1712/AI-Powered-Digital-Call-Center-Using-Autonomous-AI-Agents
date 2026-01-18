<<<<<<< HEAD
<<<<<<< HEAD
# AI-Powered-Digital-Call-Center-Using-Autonomous-AI-Agents
=======
# AI Digital Call Center - Enterprise Multi-Agent System

> **A fully functional, enterprise-grade AI-powered digital call center solution featuring autonomous multi-agent architecture for intelligent customer support.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Dashboard](#dashboard)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**AI Digital Call Center** is an enterprise-level solution that transforms traditional customer support into an intelligent, scalable, and autonomous system. Built with a multi-agent AI architecture, it handles voice, chat, email, and messaging channels with minimal human intervention while ensuring quality, compliance, and intelligent escalation.

### Key Highlights

- **Multi-Agent AI System**: Three-tier agent architecture (Primary, Supervisor, Escalation)
- **Intelligent Routing**: Context-aware message routing with confidence-based decision making
- **Real-time Analytics**: Comprehensive dashboard with CSAT, resolution time, and escalation metrics
- **Enterprise-Ready**: Production-grade code with proper error handling and scalability considerations
- **No External Dependencies**: Works with mock LLM for local development (no API keys required)

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Interface                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Streamlit  │  │  REST API    │  │   Webhooks   │     │
│  │   Chat UI    │  │   (FastAPI)  │  │   (Future)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 API Layer (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Conversation Service (Orchestrator)          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│    Multi-Agent System      │  │   Supporting Services     │
│                            │  │                           │
│  ┌───────────────────┐    │  │  • Intent Detection      │
│  │  Primary Agent    │────┼──┤  • Sentiment Analysis    │
│  │  (First Line)     │    │  │  • LLM Service           │
│  └───────────────────┘    │  │  • Confidence Scoring    │
│           │                │  └───────────────────────────┘
│           │ (if escalates) │
│  ┌───────────────────┐    │
│  │ Supervisor Agent  │────┼──┐
│  │  (Complex Queries)│    │  │
│  └───────────────────┘    │  │
│           │                │  │
│           │ (if escalates) │  │
│  ┌───────────────────┐    │  │
│  │ Escalation Agent  │────┼──┤
│  │ (Human Handoff)   │    │  │
│  └───────────────────┘    │  │
└───────────────────────────┘  │
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Persistence Layer                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SQLite / PostgreSQL                     │   │
│  │  • Conversations  • Messages  • Feedback            │   │
│  │  • Agent Metrics  • Analytics Data                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Agent Flow

```
Customer Message
      │
      ▼
┌─────────────────┐
│  Primary Agent  │ ────► Confidence Check
└─────────────────┘
      │
      ├─ High Confidence (>70%) ──► Respond & Continue
      │
      └─ Low Confidence (<70%) ──► Escalate
                                    │
                                    ▼
                          ┌──────────────────┐
                          │ Supervisor Agent │ ────► Enhanced Context
                          └──────────────────┘
                                    │
                                    ├─ Can Handle ──► Resolve
                                    │
                                    └─ Needs Human ──► Escalate
                                                          │
                                                          ▼
                                                ┌──────────────────┐
                                                │ Escalation Agent │
                                                │  (Human Handoff) │
                                                └──────────────────┘
```

---

## ✨ Features

### 🤖 Multi-Agent AI System

- **Primary Agent**: First-line support handling routine inquiries
- **Supervisor Agent**: Complex queries with enhanced context understanding
- **Escalation Agent**: Seamless handoff to human agents when needed

### 🧠 Intelligence Features

- **Intent Detection**: Rule-based + NLP pattern matching (10+ intent categories)
- **Sentiment Analysis**: Real-time sentiment scoring and classification
- **Confidence Scoring**: Agent confidence calculation for each response (0-100%)
- **Context Memory**: Full conversation history maintained across sessions
- **Intelligent Escalation**: Multi-factor escalation decision logic

### 📊 Analytics & Metrics

- **CSAT Tracking**: Customer Satisfaction Score collection and analysis
- **Resolution Time**: Average time to resolution metrics
- **Agent Performance**: Confidence scores and handling rates by agent type
- **Escalation Rate**: Percentage of conversations escalated to human agents
- **Real-time Dashboard**: Live metrics visualization with Plotly charts

### 🔧 Technical Features

- **RESTful API**: FastAPI-based backend with OpenAPI documentation
- **Database Persistence**: SQLite (development) / PostgreSQL (production)
- **Session Management**: Unique session IDs for conversation tracking
- **Error Handling**: Comprehensive error handling and logging
- **Mock LLM Support**: Works without external API keys for development

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: SQLite (SQLAlchemy ORM)
- **AI/ML**: Custom rule-based + Mock LLM (OpenAI-compatible interface)

### Frontend
- **Framework**: Streamlit 1.28+
- **Visualization**: Plotly
- **HTTP Client**: Requests

### Infrastructure
- **Containerization**: Docker (optional)
- **API Documentation**: FastAPI auto-generated OpenAPI/Swagger

---

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # API endpoints
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py      # Base agent class
│   │   │   ├── primary_agent.py   # Primary AI agent
│   │   │   ├── supervisor_agent.py # Supervisor AI agent
│   │   │   └── escalation_agent.py # Escalation agent
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Configuration settings
│   │   │   └── database.py        # Database connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── database_models.py # SQLAlchemy models
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── conversation_service.py # Conversation orchestration
│   │       ├── intent_service.py       # Intent detection
│   │       ├── sentiment_service.py    # Sentiment analysis
│   │       └── llm_service.py          # LLM integration
│   └── main.py                       # FastAPI application
│
├── frontend/
│   ├── chat_interface.py          # Streamlit chat UI
│   └── dashboard.py               # Analytics dashboard
│
├── scripts/
│   └── seed_data.py               # Sample data seeding script
│
├── database/                      # Database directory (auto-created)
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd DECODE
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be automatically created on first run. To seed sample data:

```bash
python scripts/seed_data.py
```

---

## 💻 Usage

### Running the Backend API

```bash
# From project root
cd backend
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or from project root
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

**API Documentation** (Swagger UI): `http://localhost:8000/docs`
**Alternative Docs** (ReDoc): `http://localhost:8000/redoc`

### Running the Chat Interface

```bash
# In a new terminal, with virtual environment activated
streamlit run frontend/chat_interface.py
```

The chat interface will open in your browser at: `http://localhost:8501`

### Running the Analytics Dashboard

```bash
# In a new terminal, with virtual environment activated
streamlit run frontend/dashboard.py
```

The dashboard will open in your browser at: `http://localhost:8502` (or next available port)

**Note**: You can run chat interface and dashboard on different ports by specifying:
```bash
streamlit run frontend/chat_interface.py --server.port 8501
streamlit run frontend/dashboard.py --server.port 8502
```

---

## 📡 API Documentation

### Endpoints

#### `POST /api/v1/chat`
Send a customer message and receive AI agent response.

**Request Body:**
```json
{
  "message": "I need help with my order",
  "session_id": "optional-session-id",
  "customer_id": "optional-customer-id"
}
```

**Response:**
```json
{
  "session_id": "unique-session-id",
  "response": "I'd be happy to help you with your order...",
  "agent_type": "primary",
  "agent_name": "Primary Agent",
  "confidence": 0.85,
  "intent": "order_inquiry",
  "intent_label": "Order Inquiry",
  "sentiment_score": 0.2,
  "sentiment_label": "neutral",
  "needs_escalation": false,
  "escalation_reason": null,
  "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /api/v1/conversation/{session_id}`
Get conversation history by session ID.

#### `POST /api/v1/feedback`
Submit customer satisfaction feedback (CSAT).

**Request Body:**
```json
{
  "session_id": "session-id",
  "csat_score": 5,
  "feedback_text": "Great service!"
}
```

#### `GET /api/v1/analytics`
Get analytics and metrics for dashboard.

#### `GET /api/v1/health`
Health check endpoint.

---

## 📊 Dashboard

The analytics dashboard provides:

1. **Key Performance Indicators (KPIs)**
   - Total Conversations
   - Resolved Conversations
   - Escalated Conversations
   - Average CSAT Score
   - Average Confidence Score

2. **Visualizations**
   - Conversations by Agent Type (Bar Chart)
   - Conversations by Intent (Pie Chart)
   - Conversations by Sentiment (Bar Chart)

3. **Performance Metrics**
   - Average Resolution Time
   - Escalation Rate
   - Resolution Rate

4. **Raw Data Export**
   - JSON export of all analytics data

---

## 🧪 Testing

### Manual Testing

1. Start the backend API
2. Use the Streamlit chat interface to send test messages
3. Check agent responses and escalation behavior
4. View analytics in the dashboard

### Test Scenarios

**Scenario 1: Simple Query (Primary Agent)**
- Message: "Hello, I need help with my order"
- Expected: Primary Agent responds with high confidence

**Scenario 2: Complex Query (Supervisor Escalation)**
- Message: "I'm very unhappy with my purchase and want a refund"
- Expected: Escalates to Supervisor Agent

**Scenario 3: Human Escalation**
- Message: "I want to speak to a human manager"
- Expected: Escalates to Human Agent (simulated)

**Scenario 4: Feedback Submission**
- Use API endpoint to submit CSAT feedback
- Verify feedback appears in analytics

---

## 🐳 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t ai-call-center .

# Run container
docker run -p 8000:8000 ai-call-center

# Or use Docker Compose
docker-compose up -d
```

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL
2. **LLM Integration**: Configure real OpenAI API key (set `USE_MOCK_LLM=False`)
3. **Environment Variables**: Use `.env` file for sensitive configuration
4. **Reverse Proxy**: Use Nginx or similar for production
5. **SSL/TLS**: Enable HTTPS for secure connections
6. **Monitoring**: Add logging and monitoring tools (e.g., Prometheus, Grafana)
7. **Scalability**: Deploy multiple API instances behind a load balancer

---

## 🎯 Use Cases

- **Customer Support**: 24/7 automated customer service
- **Order Inquiries**: Handle order status and tracking requests
- **Technical Support**: First-line technical issue resolution
- **Account Management**: Password resets, account inquiries
- **Billing Support**: Payment and invoice inquiries
- **Complaint Handling**: Escalation workflow for complaints
- **Feedback Collection**: CSAT and customer feedback automation

---

## 🔮 Future Enhancements

- Voice channel integration (telephony)
- Email channel support
- Multi-language support
- Integration with CRM systems
- Advanced analytics with ML models
- Real-time agent monitoring
- Custom agent training interface
- A/B testing for agent responses
- Webhook integrations
- Advanced NLP models (BERT, GPT-4)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

- **Team Name**: [Your Team Name]
- **Hackathon**: TCS DECODE / SolveSphere
- **Problem Statement**: P1 - AI-Powered Digital Call Center Using Autonomous AI Agents

---

## 📞 Support

For questions or issues, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for TCS DECODE / SolveSphere Hackathon**


>>>>>>> cb5c665 (AI-Powered-Digital-Call-Center-Using-Autonomous-AI-Agents)
=======
# AI Digital Call Center - Enterprise Multi-Agent System

> **A fully functional, enterprise-grade AI-powered digital call center solution featuring autonomous multi-agent architecture for intelligent customer support.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Dashboard](#dashboard)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**AI Digital Call Center** is an enterprise-level solution that transforms traditional customer support into an intelligent, scalable, and autonomous system. Built with a multi-agent AI architecture, it handles voice, chat, email, and messaging channels with minimal human intervention while ensuring quality, compliance, and intelligent escalation.

### Key Highlights

- **Multi-Agent AI System**: Three-tier agent architecture (Primary, Supervisor, Escalation)
- **Intelligent Routing**: Context-aware message routing with confidence-based decision making
- **Real-time Analytics**: Comprehensive dashboard with CSAT, resolution time, and escalation metrics
- **Enterprise-Ready**: Production-grade code with proper error handling and scalability considerations
- **No External Dependencies**: Works with mock LLM for local development (no API keys required)

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Interface                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Streamlit  │  │  REST API    │  │   Webhooks   │     │
│  │   Chat UI    │  │   (FastAPI)  │  │   (Future)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 API Layer (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Conversation Service (Orchestrator)          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│    Multi-Agent System      │  │   Supporting Services     │
│                            │  │                           │
│  ┌───────────────────┐    │  │  • Intent Detection      │
│  │  Primary Agent    │────┼──┤  • Sentiment Analysis    │
│  │  (First Line)     │    │  │  • LLM Service           │
│  └───────────────────┘    │  │  • Confidence Scoring    │
│           │                │  └───────────────────────────┘
│           │ (if escalates) │
│  ┌───────────────────┐    │
│  │ Supervisor Agent  │────┼──┐
│  │  (Complex Queries)│    │  │
│  └───────────────────┘    │  │
│           │                │  │
│           │ (if escalates) │  │
│  ┌───────────────────┐    │  │
│  │ Escalation Agent  │────┼──┤
│  │ (Human Handoff)   │    │  │
│  └───────────────────┘    │  │
└───────────────────────────┘  │
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Persistence Layer                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SQLite / PostgreSQL                     │   │
│  │  • Conversations  • Messages  • Feedback            │   │
│  │  • Agent Metrics  • Analytics Data                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Agent Flow

```
Customer Message
      │
      ▼
┌─────────────────┐
│  Primary Agent  │ ────► Confidence Check
└─────────────────┘
      │
      ├─ High Confidence (>70%) ──► Respond & Continue
      │
      └─ Low Confidence (<70%) ──► Escalate
                                    │
                                    ▼
                          ┌──────────────────┐
                          │ Supervisor Agent │ ────► Enhanced Context
                          └──────────────────┘
                                    │
                                    ├─ Can Handle ──► Resolve
                                    │
                                    └─ Needs Human ──► Escalate
                                                          │
                                                          ▼
                                                ┌──────────────────┐
                                                │ Escalation Agent │
                                                │  (Human Handoff) │
                                                └──────────────────┘
```

---

## ✨ Features

### 🤖 Multi-Agent AI System

- **Primary Agent**: First-line support handling routine inquiries
- **Supervisor Agent**: Complex queries with enhanced context understanding
- **Escalation Agent**: Seamless handoff to human agents when needed

### 🧠 Intelligence Features

- **Intent Detection**: Rule-based + NLP pattern matching (10+ intent categories)
- **Sentiment Analysis**: Real-time sentiment scoring and classification
- **Confidence Scoring**: Agent confidence calculation for each response (0-100%)
- **Context Memory**: Full conversation history maintained across sessions
- **Intelligent Escalation**: Multi-factor escalation decision logic

### 📊 Analytics & Metrics

- **CSAT Tracking**: Customer Satisfaction Score collection and analysis
- **Resolution Time**: Average time to resolution metrics
- **Agent Performance**: Confidence scores and handling rates by agent type
- **Escalation Rate**: Percentage of conversations escalated to human agents
- **Real-time Dashboard**: Live metrics visualization with Plotly charts

### 🔧 Technical Features

- **RESTful API**: FastAPI-based backend with OpenAPI documentation
- **Database Persistence**: SQLite (development) / PostgreSQL (production)
- **Session Management**: Unique session IDs for conversation tracking
- **Error Handling**: Comprehensive error handling and logging
- **Mock LLM Support**: Works without external API keys for development

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: SQLite (SQLAlchemy ORM)
- **AI/ML**: Custom rule-based + Mock LLM (OpenAI-compatible interface)

### Frontend
- **Framework**: Streamlit 1.28+
- **Visualization**: Plotly
- **HTTP Client**: Requests

### Infrastructure
- **Containerization**: Docker (optional)
- **API Documentation**: FastAPI auto-generated OpenAPI/Swagger

---

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py          # API endpoints
│   │   │   └── schemas.py         # Pydantic models
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py      # Base agent class
│   │   │   ├── primary_agent.py   # Primary AI agent
│   │   │   ├── supervisor_agent.py # Supervisor AI agent
│   │   │   └── escalation_agent.py # Escalation agent
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # Configuration settings
│   │   │   └── database.py        # Database connection
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── database_models.py # SQLAlchemy models
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── conversation_service.py # Conversation orchestration
│   │       ├── intent_service.py       # Intent detection
│   │       ├── sentiment_service.py    # Sentiment analysis
│   │       └── llm_service.py          # LLM integration
│   └── main.py                       # FastAPI application
│
├── frontend/
│   ├── chat_interface.py          # Streamlit chat UI
│   └── dashboard.py               # Analytics dashboard
│
├── scripts/
│   └── seed_data.py               # Sample data seeding script
│
├── database/                      # Database directory (auto-created)
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd DECODE
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be automatically created on first run. To seed sample data:

```bash
python scripts/seed_data.py
```

---

## 💻 Usage

### Running the Backend API

```bash
# From project root
cd backend
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or from project root
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

**API Documentation** (Swagger UI): `http://localhost:8000/docs`
**Alternative Docs** (ReDoc): `http://localhost:8000/redoc`

### Running the Chat Interface

```bash
# In a new terminal, with virtual environment activated
streamlit run frontend/chat_interface.py
```

The chat interface will open in your browser at: `http://localhost:8501`

### Running the Analytics Dashboard

```bash
# In a new terminal, with virtual environment activated
streamlit run frontend/dashboard.py
```

The dashboard will open in your browser at: `http://localhost:8502` (or next available port)

**Note**: You can run chat interface and dashboard on different ports by specifying:
```bash
streamlit run frontend/chat_interface.py --server.port 8501
streamlit run frontend/dashboard.py --server.port 8502
```

---

## 📡 API Documentation

### Endpoints

#### `POST /api/v1/chat`
Send a customer message and receive AI agent response.

**Request Body:**
```json
{
  "message": "I need help with my order",
  "session_id": "optional-session-id",
  "customer_id": "optional-customer-id"
}
```

**Response:**
```json
{
  "session_id": "unique-session-id",
  "response": "I'd be happy to help you with your order...",
  "agent_type": "primary",
  "agent_name": "Primary Agent",
  "confidence": 0.85,
  "intent": "order_inquiry",
  "intent_label": "Order Inquiry",
  "sentiment_score": 0.2,
  "sentiment_label": "neutral",
  "needs_escalation": false,
  "escalation_reason": null,
  "timestamp": "2024-01-15T10:30:00"
}
```

#### `GET /api/v1/conversation/{session_id}`
Get conversation history by session ID.

#### `POST /api/v1/feedback`
Submit customer satisfaction feedback (CSAT).

**Request Body:**
```json
{
  "session_id": "session-id",
  "csat_score": 5,
  "feedback_text": "Great service!"
}
```

#### `GET /api/v1/analytics`
Get analytics and metrics for dashboard.

#### `GET /api/v1/health`
Health check endpoint.

---

## 📊 Dashboard

The analytics dashboard provides:

1. **Key Performance Indicators (KPIs)**
   - Total Conversations
   - Resolved Conversations
   - Escalated Conversations
   - Average CSAT Score
   - Average Confidence Score

2. **Visualizations**
   - Conversations by Agent Type (Bar Chart)
   - Conversations by Intent (Pie Chart)
   - Conversations by Sentiment (Bar Chart)

3. **Performance Metrics**
   - Average Resolution Time
   - Escalation Rate
   - Resolution Rate

4. **Raw Data Export**
   - JSON export of all analytics data

---

## 🧪 Testing

### Manual Testing

1. Start the backend API
2. Use the Streamlit chat interface to send test messages
3. Check agent responses and escalation behavior
4. View analytics in the dashboard

### Test Scenarios

**Scenario 1: Simple Query (Primary Agent)**
- Message: "Hello, I need help with my order"
- Expected: Primary Agent responds with high confidence

**Scenario 2: Complex Query (Supervisor Escalation)**
- Message: "I'm very unhappy with my purchase and want a refund"
- Expected: Escalates to Supervisor Agent

**Scenario 3: Human Escalation**
- Message: "I want to speak to a human manager"
- Expected: Escalates to Human Agent (simulated)

**Scenario 4: Feedback Submission**
- Use API endpoint to submit CSAT feedback
- Verify feedback appears in analytics

---

## 🐳 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t ai-call-center .

# Run container
docker run -p 8000:8000 ai-call-center

# Or use Docker Compose
docker-compose up -d
```

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL
2. **LLM Integration**: Configure real OpenAI API key (set `USE_MOCK_LLM=False`)
3. **Environment Variables**: Use `.env` file for sensitive configuration
4. **Reverse Proxy**: Use Nginx or similar for production
5. **SSL/TLS**: Enable HTTPS for secure connections
6. **Monitoring**: Add logging and monitoring tools (e.g., Prometheus, Grafana)
7. **Scalability**: Deploy multiple API instances behind a load balancer

---

## 🎯 Use Cases

- **Customer Support**: 24/7 automated customer service
- **Order Inquiries**: Handle order status and tracking requests
- **Technical Support**: First-line technical issue resolution
- **Account Management**: Password resets, account inquiries
- **Billing Support**: Payment and invoice inquiries
- **Complaint Handling**: Escalation workflow for complaints
- **Feedback Collection**: CSAT and customer feedback automation

---

## 🔮 Future Enhancements

- Voice channel integration (telephony)
- Email channel support
- Multi-language support
- Integration with CRM systems
- Advanced analytics with ML models
- Real-time agent monitoring
- Custom agent training interface
- A/B testing for agent responses
- Webhook integrations
- Advanced NLP models (BERT, GPT-4)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For questions or issues, please open an issue in the repository or contact the development team.

---

**Built with ❤️ by Dheeraj Yadav**


>>>>>>> (AI-Powered-Digital-Call-Center-Using-Autonomous-AI-Agents)



>>>>>>> 14261b37bf416f59722dd19c404a8f4e82e65a92
