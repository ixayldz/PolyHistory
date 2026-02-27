<p align="center">
  <img src="https://via.placeholder.com/200x200?text=PolyHistory" alt="PolyHistory Logo" width="200" height="200">
</p>

<h1 align="center">PolyHistory</h1>

<p align="center">
  <strong>Evidence-First Multi-Perspective Historical Analysis Platform</strong>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-api-documentation">API</a> •
  <a href="#-contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-00a393.svg?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Next.js-14+-000000.svg?logo=next.js&logoColor=white" alt="Next.js 14">
  <img src="https://img.shields.io/badge/PostgreSQL-16+-336791.svg?logo=postgresql&logoColor=white" alt="PostgreSQL 16">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
</p>

---

## 📖 Overview

**PolyHistory** is an AI-powered historical research platform that eliminates ideological echo chambers by enforcing strict **evidence-first** principles and **multi-perspective** analysis.

### 🎯 Core Philosophy

> **"No Citation, No Claim"** — Every assertion must be backed by verifiable evidence from diverse sources.

### 🌍 Why PolyHistory?

Traditional historical research often suffers from:
- **Single-perspective bias** — Limited to one nation's narrative
- **Source conflation** — No distinction between primary archives and press discourse
- **Opaque reasoning** — Hidden biases and unverifiable claims

PolyHistory solves these with:
- ✅ **Multi-model consensus** — 3 independent AI judges analyze evidence
- ✅ **Cross-national comparison** — Synchronized multi-language source retrieval
- ✅ **Source hierarchy** — Primary > Academic > Secondary > Memoir > Press
- ✅ **Full auditability** — Complete chain from query to conclusion

---

## ✨ Features

### 🔍 Evidence-First Architecture

| Feature | Description |
|---------|-------------|
| **Strict Citation Requirement** | Every claim must reference specific evidence |
| **Source Reliability Scoring** | Multi-factor scoring (type, institution, consistency) |
| **Semantic Search** | Vector embeddings for relevant evidence retrieval |
| **Complete Audit Trail** | Immutable case files with deterministic replay |

### 🧠 Multi-Model Consensus

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Gemini     │    │    GPT-5.2   │    │    Claude    │
│  3.1 Pro     │    │   (OpenAI)   │    │ Opus 4.6     │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Consensus  │
                    │   Engine    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Final    │
                    │   Verdict   │
                    └─────────────┘
```

**Algorithm:**
```
Final_Score = Agreement_Ratio × Evidence_Strength

Agreement_Ratio = Supporting_Models / Total_Models
Evidence_Strength = Σ(Source_Type_Weight × Reliability)
```

### ⚖️ Balance Protocol (MBR)

Every analysis must satisfy **Minimum Balance Requirements**:

| Requirement | Minimum | Purpose |
|-------------|---------|---------|
| Turkish Sources | ≥ 2 (pro + contra) | Local perspective diversity |
| Foreign Countries | ≥ 2 | Cross-national validation |
| Press Sources | ≥ 1 per cluster | Discourse evidence |
| Primary/Academic | ≥ 1 per cluster | Authoritative evidence |

### 🌐 Multi-Lingual Support

- 🇹🇷 **Turkish (TR)** — Ottoman/Turkish Republic archives
- 🇬🇧 **English (EN)** — British/American diplomatic records
- 🇫🇷 **French (FR)** — European diplomatic correspondence
- 🇬🇷 **Greek (EL)** — Balkan/Mediterranean sources

**Period Terminology Mapping:**
```
"Angora Government" ↔ "Ankara Government"
"Mustafa Kemal" ↔ "Kemal Pasha" ↔ "Atatürk"
```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Next.js)                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/WebSocket
┌─────────────────────────────▼───────────────────────────────────┐
│                      API Gateway (FastAPI)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │    Auth     │  │    Cases    │  │    Evidence/Timeline    │  │
│  │  (JWT)      │  │   (CRUD)    │  │      (Analysis)         │  │
│  └─────────────┘  └──────┬──────┘  └─────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────────┐  ┌──────▼───────┐
│   Celery     │  │   Proposition   │  │   Evidence   │
│   Workers    │  │     Parser      │  │    Builder   │
└──────────────┘  └─────────────────┘  └──────────────┘
        │                  │                  │
        │         ┌────────▼────────┐         │
        │         │  Judge Panel    │         │
        │         │ ┌─────┬─────┐   │         │
        │         │ │Gemini│ GPT │   │         │
        │         │ │ 3.1  │ 5.2 │   │         │
        │         │ └─────┴─────┘   │         │
        │         │     Claude      │         │
        │         │    Opus 4.6     │         │
        │         └─────────────────┘         │
        │                  │                  │
┌───────▼──────────────────▼──────────────────▼───────┐
│              PostgreSQL + pgvector                 │
│  (Users, Cases, Evidence, Claims, Embeddings)      │
└─────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | FastAPI 0.115+ | Async Python API |
| **Database** | PostgreSQL 16 + pgvector | Vector similarity search |
| **Cache** | Redis 7 | Session & task queue |
| **Tasks** | Celery 5 | Background processing |
| **ORM** | SQLAlchemy 2.0 | Database abstraction |
| **Validation** | Pydantic V2 | Request/response schemas |
| **AI Models** | Gemini 3.1, GPT-5.2, Claude Opus 4.6 | Analysis judges |
| **Embeddings** | sentence-transformers | Semantic search |
| **Testing** | pytest + pytest-asyncio | Unit & integration tests |

#### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | Next.js 14 (App Router) | React framework |
| **Language** | TypeScript 5.3 | Type safety |
| **Styling** | Tailwind CSS 3.4 | Utility-first CSS |
| **State** | Zustand + React Query | Client & server state |
| **UI** | shadcn/ui | Accessible components |
| **Viz** | D3.js + Recharts | Timeline & charts |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 24.0+
- [Docker Compose](https://docs.docker.com/compose/install/) 2.20+
- [Node.js](https://nodejs.org/) 20+ (for frontend development)

### 1. Clone Repository

```bash
git clone https://github.com/your-org/polyhistory.git
cd polyhistory
```

### 2. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit with your API keys
nano .env
```

**Required API Keys:**
- [Google AI (Gemini)](https://makersuite.google.com/app/apikey)
- [OpenAI (GPT-5.2)](https://platform.openai.com/api-keys)
- [Anthropic (Claude)](https://console.anthropic.com/settings/keys)

### 3. Start Backend Services

```bash
docker-compose up -d
```

Services started:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 4. Start Frontend (Optional)

```bash
cd apps/web
npm install
npm run dev
```

Frontend: http://localhost:3000

---

## 📚 API Documentation

### Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

### Create Analysis

```bash
curl -X POST http://localhost:8000/api/v1/cases \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "proposition": "Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?",
    "time_window": {
      "start": "1919-05-01",
      "end": "1923-10-29"
    },
    "options": {
      "require_steel_man": true,
      "languages": ["tr", "en"]
    }
  }'
```

### Get Results

```bash
# Get case details
curl http://localhost:8000/api/v1/cases/{case_id} \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get evidence pack
curl http://localhost:8000/api/v1/cases/{case_id}/evidence \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get consensus analysis
curl http://localhost:8000/api/v1/cases/{case_id}/consensus \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Full API Reference:** http://localhost:8000/docs

---

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
docker-compose exec api pytest

# With coverage report
docker-compose exec api pytest --cov=app --cov-report=html

# Specific test categories
docker-compose exec api pytest tests/unit/ -v
docker-compose exec api pytest tests/integration/ -v

# Specific test file
docker-compose exec api pytest tests/unit/test_ai_integration.py -v
```

### Test Coverage

| Category | Tests | Coverage |
|----------|-------|----------|
| Authentication | 9 | ✅ Complete |
| Case Management | 10 | ✅ Complete |
| AI Integration | 30+ | ✅ Complete |
| Retrieval Services | 20+ | ✅ Complete |
| **Total** | **80+** | **~85%** |

---

## 📁 Project Structure

```
polyhistory/
├── 📄 README.md                    # This file
├── 📄 prd.md                       # Product Requirements Document
├── 📄 implementation-plan.md       # Technical implementation guide
├── 📄 .env.example                 # Environment configuration template
├── 🐳 docker-compose.yml           # Development orchestration
│
├── apps/
│   ├── api/                        # 🐍 FastAPI Backend
│   │   ├── app/
│   │   │   ├── main.py             # Application entry
│   │   │   ├── core/               # Config, database, security
│   │   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── schemas/            # Pydantic validation schemas
│   │   │   ├── api/v1/endpoints/   # REST API routes
│   │   │   ├── services/           # Business logic
│   │   │   │   ├── judge/          # 🤖 AI model adapters
│   │   │   │   │   ├── base.py     # Abstract base class
│   │   │   │   │   ├── gemini.py   # Google Gemini 3.1 Pro
│   │   │   │   │   ├── gpt.py      # OpenAI GPT-5.2
│   │   │   │   │   ├── claude.py   # Anthropic Claude Opus 4.6
│   │   │   │   │   └── orchestrator.py
│   │   │   │   ├── proposition_parser.py
│   │   │   │   ├── query_expansion.py
│   │   │   │   ├── evidence_builder.py
│   │   │   │   ├── balance_protocol.py
│   │   │   │   └── consensus_engine.py
│   │   │   └── tasks/              # Celery background tasks
│   │   ├── tests/                  # 🧪 Test suite
│   │   │   ├── unit/
│   │   │   └── integration/
│   │   └── Dockerfile
│   │
│   └── web/                        # ⚛️ Next.js Frontend
│       ├── app/                    # App Router (Next.js 14)
│       ├── components/
│       ├── lib/
│       └── package.json
│
└── packages/                       # 📦 Shared packages (future)
```

---

## 🔬 How It Works

### 1. Proposition Parsing

```python
# Input
"Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?"

# Output
{
  "entities": ["Mustafa Kemal", "İngiltere"],
  "time_window": {"start": "1919-05-01", "end": "1923-10-29"},
  "geography": ["Turkey", "UK"],
  "claim_type": "diplomatic"
}
```

### 2. Evidence Retrieval

Multi-source parallel collection:
- 📚 Academic databases (Semantic Scholar)
- 📰 Period press archives
- 📜 National archives (Turkish, British, French)
- 📄 Treaty/official document indices

### 3. Multi-Model Analysis

Each AI judge analyzes independently:

| Judge | Specialty |
|-------|-----------|
| **Gemini 3.1 Pro** | Broad context synthesis, multilingual |
| **GPT-5.2** | Claim decomposition, consistency checking |
| **Claude Opus 4.6** | Steel-man argumentation, nuanced interpretation |

### 4. Consensus Computation

```python
# Example calculation
Evidence_Strength = (1.0 × 0.9) + (0.4 × 0.7) = 1.18
Agreement_Ratio = 2/3 = 0.67
Final_Score = 0.67 × 1.18 = 0.79  # High confidence
```

### 5. Output Generation

```json
{
  "verdict": {
    "short_statement": "Evidence supports limited diplomatic contact...",
    "confidence_score": 79
  },
  "core_claims": [...],
  "disputed_claims": [...],
  "evidence_ledger": [...],
  "timeline": [...]
}
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **Python:** PEP 8, type hints required
- **TypeScript:** Strict mode enabled
- **Tests:** Minimum 80% coverage for new code
- **Documentation:** Update README for API changes

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** team for the excellent web framework
- **Sentence Transformers** for multilingual embeddings
- **PostgreSQL** team for pgvector extension

---

## 📞 Support

- 📧 **Email:** support@polyhistory.app
- 💬 **Discord:** [Join our community](https://discord.gg/polyhistory)
- 🐛 **Issues:** [GitHub Issues](https://github.com/your-org/polyhistory/issues)

---

<p align="center">
  <strong>PolyHistory</strong> — Making historical research transparent, unbiased, and verifiable.
</p>

<p align="center">
  Built with ❤️ for historians, researchers, and truth-seekers everywhere.
</p>
