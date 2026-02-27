# PolyHistory API

<p align="center">
  <strong>FastAPI-Powered Historical Analysis Engine</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-00a393.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-16+-336791.svg?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Coverage-85%25-green.svg" alt="Coverage">
</p>

---

## 🚀 Quick Start

### Prerequisites

- Docker 24.0+
- Docker Compose 2.20+
- API keys for AI models (see [Configuration](#%EF%B8%8F-configuration))

### 1. Setup Environment

```bash
# Copy configuration template
cp .env.example .env

# Edit with your API keys
nano .env
```

### 2. Start Services

```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs
docker-compose logs -f api
```

### 3. Access API

| Endpoint | URL |
|----------|-----|
| **API Base** | http://localhost:8000 |
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |

---

## ⚙️ Configuration

### Required Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/polyhistory

# Cache & Queue
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-super-secret-key

# AI Model API Keys (at least 2 required)
GEMINI_API_KEY=your-gemini-key
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-claude-key
```

### Getting API Keys

| Model | Provider | Link | Pricing |
|-------|----------|------|---------|
| **Gemini 3.1 Pro** | Google AI | [Get Key](https://makersuite.google.com/app/apikey) | Free tier: 60 req/min |
| **GPT-5.2** | OpenAI | [Get Key](https://platform.openai.com/api-keys) | Pay-per-use |
| **Claude Opus 4.6** | Anthropic | [Get Key](https://console.anthropic.com/settings/keys) | Pay-per-use |

---

## 🧪 Testing

### Run All Tests

```bash
docker-compose exec api pytest
```

### Run with Coverage

```bash
docker-compose exec api pytest --cov=app --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Unit tests only
docker-compose exec api pytest tests/unit/ -v

# Integration tests only
docker-compose exec api pytest tests/integration/ -v

# Specific test file
docker-compose exec api pytest tests/unit/test_ai_integration.py -v

# Specific test function
docker-compose exec api pytest tests/unit/test_auth.py::test_login_success -v
```

### Test Categories

```bash
# By marker
pytest -m unit          # Unit tests
pytest -m integration   # Integration tests
pytest -m slow          # Slow running tests
```

---

## 📁 Project Structure

```
app/
├── 📄 main.py                 # FastAPI application entry
├── 🔧 core/                   # Core utilities
│   ├── config.py             # Pydantic settings
│   ├── database.py           # SQLAlchemy & asyncpg
│   ├── security.py           # JWT & password hashing
│   └── exceptions.py         # Custom exceptions
├── 🗄️ models/                # Database models (SQLAlchemy)
│   ├── user.py
│   ├── case.py
│   ├── evidence.py
│   └── claim.py
├── 📋 schemas/               # Pydantic models
│   ├── user.py
│   ├── case.py
│   └── evidence.py
├── 🌐 api/                   # REST API routes
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py       # Authentication
│       │   ├── cases.py      # Case management
│       │   ├── evidence.py   # Evidence retrieval
│       │   ├── timeline.py   # Timeline generation
│       │   ├── consensus.py  # Consensus analysis
│       │   └── export.py     # Report export
│       └── deps.py           # Dependencies (auth, db)
├── 🤖 services/              # Business logic
│   ├── judge/                # AI model adapters
│   │   ├── base.py           # Abstract base class
│   │   ├── gemini.py         # Gemini 3.1 Pro Preview
│   │   ├── gpt.py            # GPT-5.2
│   │   ├── claude.py         # Claude Opus 4.6
│   │   └── orchestrator.py   # Parallel execution
│   ├── proposition_parser.py # NLP proposition parsing
│   ├── query_expansion.py    # Multi-lingual query expansion
│   ├── evidence_builder.py   # Evidence pack construction
│   ├── balance_protocol.py   # MBR enforcement
│   └── consensus_engine.py   # Consensus computation
├── 📦 tasks/                 # Celery background tasks
│   └── case_workflow.py      # Main analysis workflow
└── 🧪 tests/                 # Test suite
    ├── conftest.py           # Pytest configuration
    ├── unit/                 # Unit tests
    └── integration/          # Integration tests
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | User registration |
| `POST` | `/api/v1/auth/login` | User login |
| `POST` | `/api/v1/auth/refresh` | Token refresh |
| `GET` | `/api/v1/auth/me` | Current user info |

### Cases

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/cases` | Create new analysis |
| `GET` | `/api/v1/cases` | List user cases |
| `GET` | `/api/v1/cases/{id}` | Get case details |
| `DELETE` | `/api/v1/cases/{id}` | Delete case |

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/cases/{id}/evidence` | Get evidence pack |
| `GET` | `/api/v1/cases/{id}/timeline` | Get timeline data |
| `GET` | `/api/v1/cases/{id}/consensus` | Get consensus analysis |
| `POST` | `/api/v1/export/{id}` | Export report |

### Example Requests

#### Create Analysis

```bash
curl -X POST http://localhost:8000/api/v1/cases \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "proposition": "Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?",
    "time_window": {
      "start": "1919-05-01",
      "end": "1923-10-29"
    },
    "options": {
      "require_steel_man": true,
      "source_preference": "balanced",
      "languages": ["tr", "en"]
    }
  }'
```

#### Get Evidence

```bash
curl "http://localhost:8000/api/v1/cases/$CASE_ID/evidence?source_type=primary&country=TR" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🏗️ Architecture

### Core Services

```
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
│   Proposition│ │  Judge     │ │  Evidence  │
│   Parser     │ │  Panel     │ │  Builder   │
└──────────────┘ └─────┬──────┘ └────────────┘
                       │
              ┌────────┼────────┐
              │        │        │
        ┌─────▼───┐ ┌──▼───┐ ┌──▼────┐
        │ Gemini  │ │ GPT  │ │ Claude│
        │ 3.1 Pro │ │ 5.2  │ │Opus   │
        └─────┬───┘ └──┬───┘ └──┬────┘
              │        │        │
              └────────┼────────┘
                       │
              ┌────────▼────────┐
              │ Consensus Engine │
              └─────────────────┘
```

### AI Models

| Model | Version | Strengths |
|-------|---------|-----------|
| **Gemini** | 3.1 Pro Preview | Broad context, multilingual |
| **GPT** | 5.2 | Claim decomposition, consistency |
| **Claude** | Opus 4.6 | Steel-man, nuanced interpretation |

---

## 🛠️ Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt -r requirements-test.txt

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Code Quality

```bash
# Run linter
flake8 app/

# Run type checker
mypy app/

# Format code
black app/
isort app/
```

### Adding New Features

1. **Add Model:** Create class in `app/services/judge/`
2. **Add Endpoint:** Create file in `app/api/v1/endpoints/`
3. **Add Tests:** Create file in `app/tests/`
4. **Update Docs:** Update this README and Swagger docs

---

## 📊 Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health
# {"status": "healthy"}

# Readiness check
curl http://localhost:8000/ready
# {"status": "ready"}
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View API logs only
docker-compose logs -f api

# View Celery worker logs
docker-compose logs -f celery
```

---

## 🐛 Troubleshooting

### Common Issues

**Database connection failed:**
```bash
# Check PostgreSQL is running
docker-compose ps db

# Check logs
docker-compose logs db
```

**AI model timeout:**
```bash
# Increase timeout in .env
MODEL_TIMEOUT_SECONDS=60
```

**Tests failing:**
```bash
# Reset test database
docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS test_polyhistory;"
docker-compose exec db psql -U postgres -c "CREATE DATABASE test_polyhistory;"
```

---

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Alternative Docs:** http://localhost:8000/redoc (ReDoc)
- **PRD:** See `../prd.md`
- **Implementation Plan:** See `../implementation-plan.md`

---

## 🤝 Contributing

See [Contributing Guide](../CONTRIBUTING.md) for details.

---

<p align="center">
  Built with ❤️ using FastAPI, PostgreSQL, and cutting-edge AI
</p>
