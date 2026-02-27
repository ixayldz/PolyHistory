# Implementation Plan (IMP)
## PolyHistory Platform — Technical Execution Roadmap

**Version:** 1.0  
**Date:** February 27, 2026  
**Status:** Ready for Development  

---

## 1. Technology Stack Specification

### 1.1 Backend Stack

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| API Framework | FastAPI | 0.115+ | Async native, auto OpenAPI, high performance |
| Language | Python | 3.11+ | AI/ML ecosystem, type hints |
| Task Queue | Celery | 5.3+ | Distributed tasks, Redis backend |
| Message Broker | Redis | 7.2+ | Celery broker + caching |
| ORM | SQLAlchemy 2.0 | 2.0+ | Async support, type safety |
| Migrations | Alembic | 1.13+ | Database versioning |
| Document DB | PostgreSQL | 16+ | JSONB, full-text search, reliability |
| Vector DB | pgvector | 0.6+ | PostgreSQL extension, single DB solution |
| HTTP Client | httpx | 0.26+ | Async HTTP for API calls |
| Validation | Pydantic V2 | 2.5+ | FastAPI native, performance |
| Testing | pytest | 8.0+ | Async support, fixtures |

### 1.2 Frontend Stack

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| Framework | Next.js (App Router) | 14+ | SSR, API routes, React 18 |
| Language | TypeScript | 5.3+ | Type safety, IDE support |
| Styling | Tailwind CSS | 3.4+ | Utility-first, rapid development |
| Components | shadcn/ui | Latest | Accessible, customizable |
| State Management | Zustand | 4.5+ | Lightweight, TypeScript native |
| Server State | TanStack Query | 5.18+ | Caching, background sync |
| Forms | React Hook Form | 7.50+ | Performance, validation |
| Visualization | D3.js + Recharts | Latest | Timeline, charts |
| PDF Generation | @react-pdf/renderer | 3.4+ | Client-side PDF export |
| Icons | Lucide React | Latest | Consistent icon set |

### 1.3 AI/ML Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Model APIs | Google AI, OpenAI, Anthropic | Gemini, GPT, Claude access |
| Embeddings | sentence-transformers | Multilingual embeddings (paraphrase-multilingual-MiniLM-L12-v2) |
| NER | spaCy + transformers | Historical entity extraction |
| NLI | transformers pipeline | Contradiction detection |
| Text Processing | LangChain | Orchestration (optional) |

### 1.4 Infrastructure Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Container | Docker | Application packaging |
| Orchestration | Docker Compose (local) / Kubernetes (prod) | Container management |
| Reverse Proxy | Traefik | Routing, SSL |
| Monitoring | Prometheus + Grafana | Metrics, dashboards |
| Logging | Loki + Grafana | Centralized logging |
| CI/CD | GitHub Actions | Automated pipelines |
| IaC | Terraform / Pulumi | Infrastructure provisioning |

---

## 2. Project Structure

### 2.1 Monorepo Organization

```
polyhistory/
├── README.md
├── docker-compose.yml
├── Makefile
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── apps/
│   ├── web/                          # Next.js frontend
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── stores/
│   │   ├── types/
│   │   └── public/
│   └── api/                          # FastAPI backend
│       ├── app/
│       │   ├── api/
│       │   ├── core/
│       │   ├── models/
│       │   ├── schemas/
│       │   ├── services/
│       │   └── tasks/
│       ├── alembic/
│       ├── tests/
│       └── Dockerfile
├── packages/
│   ├── shared-types/                 # Shared TypeScript/Python types
│   ├── ui-components/                # Shared React components
│   └── config/                       # Shared config (eslint, tsconfig)
├── infrastructure/
│   ├── terraform/
│   └── k8s/
└── docs/
    ├── api/
    └── architecture/
```

### 2.2 Backend Module Structure

```
apps/api/app/
├── __init__.py
├── main.py                          # FastAPI app entry
├── core/
│   ├── config.py                    # Pydantic Settings
│   ├── database.py                  # SQLAlchemy engine/session
│   ├── security.py                  # JWT, auth
│   └── exceptions.py                # Custom exceptions
├── api/
│   ├── deps.py                      # Dependencies (DB, auth)
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py                # API v1 aggregator
│   │   ├── endpoints/
│   │   │   ├── cases.py
│   │   │   ├── evidence.py
│   │   │   ├── timeline.py
│   │   │   ├── consensus.py
│   │   │   ├── export.py
│   │   │   └── auth.py
│   │   └── websocket/
│   │       └── case_progress.py
├── models/
│   ├── __init__.py
│   ├── base.py                      # SQLAlchemy Base
│   ├── case.py
│   ├── evidence.py
│   ├── claim.py
│   ├── user.py
│   └── audit.py
├── schemas/
│   ├── __init__.py
│   ├── case.py                      # Pydantic models
│   ├── evidence.py
│   ├── claim.py
│   ├── proposition.py
│   └── consensus.py
├── services/
│   ├── __init__.py
│   ├── proposition_parser.py
│   ├── query_expansion.py
│   ├── retrieval/
│   │   ├── academic.py
│   │   ├── archive.py
│   │   ├── press.py
│   │   └── treaty.py
│   ├── evidence_builder.py
│   ├── text_processor.py
│   ├── judge/
│   │   ├── base.py
│   │   ├── gemini.py
│   │   ├── gpt.py
│   │   ├── claude.py
│   │   └── orchestrator.py
│   ├── consensus_engine.py
│   ├── balance_protocol.py
│   └── report_generator.py
├── tasks/
│   ├── __init__.py
│   ├── case_workflow.py             # Celery tasks
│   └── periodic.py
└── utils/
    ├── text.py
    ├── validation.py
    └── embeddings.py
```

### 2.3 Frontend Module Structure

```
apps/web/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                     # Landing
│   ├── globals.css
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   ├── page.tsx                 # Dashboard home
│   │   ├── cases/
│   │   │   ├── page.tsx             # Case list
│   │   │   └── [id]/
│   │   │       ├── page.tsx         # Case detail
│   │   │       ├── evidence/
│   │   │       ├── timeline/
│   │   │       └── consensus/
│   │   └── new/
│   │       └── page.tsx             # New case form
│   ├── api/
│   │   └── auth/
│   └── auth/
│       └── callback/
├── components/
│   ├── ui/                          # shadcn components
│   ├── layout/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── footer.tsx
│   ├── cases/
│   │   ├── case-card.tsx
│   │   ├── case-form.tsx
│   │   ├── case-status.tsx
│   │   └── case-list.tsx
│   ├── evidence/
│   │   ├── evidence-panel.tsx
│   │   ├── evidence-card.tsx
│   │   ├── evidence-filter.tsx
│   │   └── snippet-viewer.tsx
│   ├── timeline/
│   │   ├── timeline.tsx
│   │   ├── timeline-track.tsx
│   │   └── timeline-controls.tsx
│   ├── consensus/
│   │   ├── consensus-panel.tsx
│   │   ├── agreement-heatmap.tsx
│   │   └── disputed-claims.tsx
│   ├── chat/
│   │   ├── chat-interface.tsx
│   │   ├── message-bubble.tsx
│   │   └── streaming-text.tsx
│   └── visualization/
│       ├── confidence-badge.tsx
│       └── source-distribution.tsx
├── lib/
│   ├── api.ts                       # API client
│   ├── utils.ts
│   ├── constants.ts
│   └── validations.ts
├── stores/
│   ├── case-store.ts
│   ├── evidence-store.ts
│   └── ui-store.ts
├── hooks/
│   ├── use-case.ts
│   ├── use-evidence.ts
│   └── use-timeline.ts
├── types/
│   ├── case.ts
│   ├── evidence.ts
│   └── api.ts
└── public/
    ├── fonts/
    └── images/
```

---

## 3. Database Schema

### 3.1 Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    users    │     │    cases    │     │ evidence_   │
├─────────────┤     ├─────────────┤     │   items     │
│ id (PK)     │◄────┤ user_id(FK) │     ├─────────────┤
│ email       │     │ id (PK)     │◄────┤ case_id(FK) │
│ tier        │     │ proposition │     │ id (PK)     │
│ created_at  │     │ status      │     │ title       │
└─────────────┘     │ time_window │     │ source_type │
                    │ confidence  │     │ country     │
                    │ verdict     │     │ language    │
                    └─────────────┘     │ reliability │
                           │            │ metadata    │
                           │            └─────────────┘
                           │                   │
                           │            ┌─────────────┐
                           │            │  snippets   │
                           │            ├─────────────┤
                           │            │ id (PK)     │
                           ▼            │ evidence_id │
                    ┌─────────────┐     │ text        │
                    │    claims   │     │ location    │
                    ├─────────────┤     │ embedding   │
                    │ id (PK)     │     │ quality     │
                    │ case_id(FK) │     └─────────────┘
                    │ text        │
                    │ category    │     ┌─────────────┐
                    │ stance      │     │   models    │
                    │ confidence  │     ├─────────────┤
                    │ is_core     │     │ id (PK)     │
                    └─────────────┘     │ case_id(FK) │
                           │            │ model_name  │
                           │            │ output_json │
                           ▼            │ latency_ms  │
                    ┌─────────────┐     └─────────────┘
                    │ claim_      │
                    │ _evidence   │
                    ├─────────────┤
                    │ claim_id(FK)│
                    │ snippet_id  │
                    │ weight      │
                    └─────────────┘
```

### 3.2 Table Definitions

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    tier VARCHAR(50) DEFAULT 'free', -- free, pro, research, enterprise
    monthly_analysis_count INTEGER DEFAULT 0,
    monthly_analysis_limit INTEGER DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### cases
```sql
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    proposition TEXT NOT NULL,
    normalized_proposition JSONB,
    time_window_start DATE,
    time_window_end DATE,
    geography VARCHAR(100)[],
    claim_type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    
    -- MBR Compliance
    mbr_compliant BOOLEAN DEFAULT FALSE,
    mbr_missing_clusters JSONB,
    
    -- Results
    verdict_short TEXT,
    confidence_score DECIMAL(5,4),
    consensus_output JSONB,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    processing_duration_ms INTEGER
);

CREATE INDEX idx_cases_user_id ON cases(user_id);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_created_at ON cases(created_at);
```

#### evidence_items
```sql
CREATE TABLE evidence_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    
    -- Source metadata
    title VARCHAR(500),
    author VARCHAR(255),
    publisher VARCHAR(255),
    publication_date DATE,
    country VARCHAR(100),
    language VARCHAR(10),
    
    -- Classification
    source_type VARCHAR(50), -- primary, secondary, press, memoir, academic
    stance VARCHAR(20), -- pro, contra, neutral
    
    -- Scoring
    reliability_score DECIMAL(5,4),
    reliability_factors JSONB,
    
    -- Reference
    url TEXT,
    archive_id VARCHAR(255),
    biblio_reference TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_evidence_case_id ON evidence_items(case_id);
CREATE INDEX idx_evidence_type ON evidence_items(source_type);
CREATE INDEX idx_evidence_country ON evidence_items(country);
CREATE INDEX idx_evidence_stance ON evidence_items(stance);
```

#### snippets
```sql
CREATE TABLE snippets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID REFERENCES evidence_items(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    page_location VARCHAR(100),
    paragraph_number INTEGER,
    quality_score DECIMAL(5,4),
    
    -- Vector embedding for semantic search
    embedding VECTOR(384), -- paraphrase-multilingual-MiniLM-L12-v2
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_snippets_evidence ON snippets(evidence_id);
-- HNSW index for vector similarity search
CREATE INDEX idx_snippets_embedding ON snippets 
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

#### claims
```sql
CREATE TABLE claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    claim_id_in_case VARCHAR(100),
    normalized_text TEXT NOT NULL,
    category VARCHAR(50), -- diplomatic, economic, military, intelligence, propaganda
    stance VARCHAR(20), -- support, oppose, neutral
    
    -- Consensus scoring
    evidence_strength DECIMAL(5,4),
    agreement_ratio DECIMAL(5,4),
    final_score DECIMAL(5,4),
    confidence_label VARCHAR(20), -- low, medium, high
    
    -- Status
    is_core_consensus BOOLEAN DEFAULT FALSE,
    is_disputed BOOLEAN DEFAULT FALSE,
    dispute_reasons JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_claims_case_id ON claims(case_id);
CREATE INDEX idx_claims_stance ON claims(stance);
CREATE INDEX idx_claims_confidence ON claims(confidence_label);
```

#### claim_evidence
```sql
CREATE TABLE claim_evidence (
    claim_id UUID REFERENCES claims(id) ON DELETE CASCADE,
    snippet_id UUID REFERENCES snippets(id) ON DELETE CASCADE,
    evidence_weight DECIMAL(5,4),
    is_counter_evidence BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (claim_id, snippet_id)
);
```

#### model_outputs
```sql
CREATE TABLE model_outputs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL, -- gemini, gpt, claude
    output_json JSONB NOT NULL,
    latency_ms INTEGER,
    token_count INTEGER,
    status VARCHAR(50), -- success, timeout, error
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_model_outputs_case ON model_outputs(case_id);
```

#### audit_logs
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID REFERENCES cases(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_case ON audit_logs(case_id);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
```

---

## 4. API Specification

### 4.1 OpenAPI Schema

```yaml
openapi: 3.0.3
info:
  title: PolyHistory API
  version: 1.0.0
  description: Evidence-first historical analysis platform API

paths:
  /api/v1/cases:
    post:
      summary: Create new analysis case
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [proposition]
              properties:
                proposition:
                  type: string
                  example: "Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?"
                time_window:
                  type: object
                  properties:
                    start: { type: string, format: date }
                    end: { type: string, format: date }
                geography:
                  type: array
                  items: { type: string }
                options:
                  type: object
                  properties:
                    require_steel_man: { type: boolean, default: true }
                    source_preference: { 
                      type: string, 
                      enum: [primary_only, balanced, broad],
                      default: balanced
                    }
                    languages:
                      type: array
                      items: { type: string, enum: [tr, en, fr, el] }
      responses:
        201:
          description: Case created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Case'

    get:
      summary: List user cases
      parameters:
        - name: status
          in: query
          schema: { type: string }
        - name: limit
          in: query
          schema: { type: integer, default: 20 }
        - name: offset
          in: query
          schema: { type: integer, default: 0 }
      responses:
        200:
          description: Cases list
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items: { $ref: '#/components/schemas/Case' }
                  total: { type: integer }

  /api/v1/cases/{case_id}:
    get:
      summary: Get case details
      parameters:
        - name: case_id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        200:
          description: Case details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CaseDetail'

  /api/v1/cases/{case_id}/evidence:
    get:
      summary: Get evidence pack
      parameters:
        - name: case_id
          in: path
          required: true
          schema: { type: string, format: uuid }
        - name: source_type
          in: query
          schema: { type: string }
        - name: country
          in: query
          schema: { type: string }
        - name: stance
          in: query
          schema: { type: string }
      responses:
        200:
          description: Evidence items
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/EvidenceItem' }

  /api/v1/cases/{case_id}/timeline:
    get:
      summary: Get timeline data
      parameters:
        - name: case_id
          in: path
          required: true
          schema: { type: string, format: uuid }
        - name: granularity
          in: query
          schema: { 
            type: string, 
            enum: [day, week, month, year],
            default: month
          }
      responses:
        200:
          description: Timeline events
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/TimelineEvent' }

  /api/v1/cases/{case_id}/consensus:
    get:
      summary: Get consensus analysis
      parameters:
        - name: case_id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        200:
          description: Consensus data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConsensusAnalysis'

  /api/v1/cases/{case_id}/export:
    post:
      summary: Export case report
      parameters:
        - name: case_id
          in: path
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                format: { 
                  type: string, 
                  enum: [markdown, pdf, json],
                  default: markdown
                }
                citation_style: {
                  type: string,
                  enum: [apa, chicago],
                  default: chicago
                }
      responses:
        200:
          description: Exported report
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary

  /api/v1/auth/register:
    post:
      summary: Register new user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 8 }
      responses:
        201:
          description: User created

  /api/v1/auth/login:
    post:
      summary: Login user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string }
                password: { type: string }
      responses:
        200:
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }
                  token_type: { type: string, default: bearer }

components:
  schemas:
    Case:
      type: object
      properties:
        id: { type: string, format: uuid }
        proposition: { type: string }
        status: { type: string }
        confidence_score: { type: number }
        created_at: { type: string, format: date-time }
    
    CaseDetail:
      allOf:
        - $ref: '#/components/schemas/Case'
        - type: object
          properties:
            normalized_proposition: { type: object }
            time_window: { type: object }
            mbr_compliant: { type: boolean }
            verdict: { type: object }
            consensus: { type: object }
    
    EvidenceItem:
      type: object
      properties:
        id: { type: string }
        title: { type: string }
        source_type: { type: string }
        country: { type: string }
        language: { type: string }
        reliability_score: { type: number }
        stance: { type: string }
        snippets:
          type: array
          items: { $ref: '#/components/schemas/Snippet' }
    
    Snippet:
      type: object
      properties:
        id: { type: string }
        text: { type: string }
        page_location: { type: string }
        quality_score: { type: number }
    
    TimelineEvent:
      type: object
      properties:
        date: { type: string, format: date }
        track: { type: string }
        events:
          type: array
          items:
            type: object
            properties:
              title: { type: string }
              description: { type: string }
              source_id: { type: string }
    
    ConsensusAnalysis:
      type: object
      properties:
        core_claims:
          type: array
          items: { $ref: '#/components/schemas/Claim' }
        disputed_claims:
          type: array
          items: { $ref: '#/components/schemas/Claim' }
        agreement_matrix: { type: object }
    
    Claim:
      type: object
      properties:
        id: { type: string }
        text: { type: string }
        category: { type: string }
        stance: { type: string }
        confidence_label: { type: string }
        final_score: { type: number }
        evidence_refs:
          type: array
          items: { type: object }
```

---

## 5. Frontend Architecture

### 5.1 State Management

```typescript
// stores/case-store.ts
import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'

interface CaseState {
  currentCase: Case | null
  evidence: EvidenceItem[]
  claims: Claim[]
  timeline: TimelineEvent[]
  isLoading: boolean
  error: string | null
  
  // Actions
  createCase: (proposition: string, options: CaseOptions) => Promise<void>
  fetchCase: (id: string) => Promise<void>
  fetchEvidence: (filters: EvidenceFilters) => Promise<void>
  fetchTimeline: (granularity: Granularity) => Promise<void>
  subscribeToProgress: (caseId: string) => () => void
}

export const useCaseStore = create<CaseState>()(
  immer((set, get) => ({
    currentCase: null,
    evidence: [],
    claims: [],
    timeline: [],
    isLoading: false,
    error: null,
    
    createCase: async (proposition, options) => {
      set({ isLoading: true })
      try {
        const response = await api.post('/cases', { proposition, ...options })
        set({ currentCase: response.data })
        // Subscribe to WebSocket for progress updates
        get().subscribeToProgress(response.data.id)
      } catch (error) {
        set({ error: error.message })
      } finally {
        set({ isLoading: false })
      }
    },
    
    // ... other actions
  }))
)
```

### 5.2 Key Components

#### Chat Interface with Streaming
```typescript
// components/chat/chat-interface.tsx
'use client'

import { useState } from 'react'
import { useCaseStore } from '@/stores/case-store'
import { MessageBubble } from './message-bubble'
import { StreamingText } from './streaming-text'

export function ChatInterface() {
  const [input, setInput] = useState('')
  const { createCase, currentCase, isLoading } = useCaseStore()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return
    
    await createCase(input, {
      require_steel_man: true,
      source_preference: 'balanced',
      languages: ['tr', 'en']
    })
    setInput('')
  }
  
  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {currentCase && (
          <MessageBubble 
            type="user" 
            content={currentCase.proposition} 
          />
        )}
        {currentCase?.status === 'processing' && (
          <StreamingText caseId={currentCase.id} />
        )}
        {currentCase?.verdict && (
          <MessageBubble 
            type="assistant" 
            content={currentCase.verdict.short_statement}
            confidence={currentCase.confidence_score}
          />
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tarihsel bir önerme yazın..."
            className="flex-1 px-4 py-2 border rounded-lg"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg"
          >
            {isLoading ? 'Analiz...' : 'Gönder'}
          </button>
        </div>
      </form>
    </div>
  )
}
```

#### Evidence Panel
```typescript
// components/evidence/evidence-panel.tsx
'use client'

import { useState } from 'react'
import { useEvidenceStore } from '@/stores/evidence-store'
import { EvidenceCard } from './evidence-card'
import { EvidenceFilter } from './evidence-filter'

export function EvidencePanel({ caseId }: { caseId: string }) {
  const [filters, setFilters] = useState({
    sourceType: '',
    country: '',
    stance: ''
  })
  
  const { evidence, isLoading } = useEvidenceStore()
  
  const filteredEvidence = evidence.filter(item => {
    if (filters.sourceType && item.source_type !== filters.sourceType) return false
    if (filters.country && item.country !== filters.country) return false
    if (filters.stance && item.stance !== filters.stance) return false
    return true
  })
  
  return (
    <div className="h-full flex flex-col">
      <EvidenceFilter 
        filters={filters} 
        onChange={setFilters}
        availableCountries={[...new Set(evidence.map(e => e.country))]}
      />
      
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {isLoading ? (
          <div className="animate-pulse space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded" />
            ))}
          </div>
        ) : (
          filteredEvidence.map(item => (
            <EvidenceCard 
              key={item.id} 
              evidence={item}
              caseId={caseId}
            />
          ))
        )}
      </div>
    </div>
  )
}
```

#### Timeline Visualization
```typescript
// components/timeline/timeline.tsx
'use client'

import { useEffect, useRef } from 'react'
import * as d3 from 'd3'
import { useTimelineStore } from '@/stores/timeline-store'

interface TimelineProps {
  caseId: string
  granularity: 'day' | 'week' | 'month' | 'year'
}

export function Timeline({ caseId, granularity }: TimelineProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const { timeline, fetchTimeline } = useTimelineStore()
  
  useEffect(() => {
    fetchTimeline(caseId, granularity)
  }, [caseId, granularity])
  
  useEffect(() => {
    if (!timeline.length || !svgRef.current) return
    
    // D3.js timeline visualization
    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()
    
    const margin = { top: 20, right: 30, bottom: 30, left: 100 }
    const width = svgRef.current.clientWidth - margin.left - margin.right
    const height = 400 - margin.top - margin.bottom
    
    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)
    
    // Scales
    const timeExtent = d3.extent(timeline, d => new Date(d.date))
    const x = d3.scaleTime()
      .domain(timeExtent as [Date, Date])
      .range([0, width])
    
    const tracks = [...new Set(timeline.map(d => d.track))]
    const y = d3.scaleBand()
      .domain(tracks)
      .range([0, height])
      .padding(0.1)
    
    // Draw axes
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
    
    g.append('g')
      .call(d3.axisLeft(y))
    
    // Draw events
    const events = g.selectAll('.event')
      .data(timeline)
      .enter()
      .append('g')
      .attr('class', 'event')
      .attr('transform', d => `translate(${x(new Date(d.date))},${y(d.track)})`)
    
    events.append('circle')
      .attr('r', 6)
      .attr('fill', d => getTrackColor(d.track))
    
    // Add tooltips, interactions...
  }, [timeline])
  
  return (
    <div className="w-full overflow-x-auto">
      <svg 
        ref={svgRef} 
        width="100%" 
        height={400}
        className="min-w-[800px]"
      />
    </div>
  )
}

function getTrackColor(track: string): string {
  const colors: Record<string, string> = {
    'TR_pro': '#22c55e',
    'TR_contra': '#ef4444',
    'UK': '#3b82f6',
    'FR': '#8b5cf6',
    'GR': '#f59e0b'
  }
  return colors[track] || '#6b7280'
}
```

### 5.3 Route Structure

```typescript
// app/(dashboard)/cases/[id]/page.tsx
export default async function CaseDetailPage({ 
  params: { id } 
}: { 
  params: { id: string } 
}) {
  return (
    <div className="h-full flex">
      {/* Left Panel - Chat */}
      <div className="w-1/2 border-r">
        <ChatInterface caseId={id} />
      </div>
      
      {/* Right Panel - Evidence/Tabs */}
      <div className="w-1/2 flex flex-col">
        <Tabs defaultValue="evidence">
          <TabsList className="w-full">
            <TabsTrigger value="evidence">Kanıtlar</TabsTrigger>
            <TabsTrigger value="timeline">Zaman Çizelgesi</TabsTrigger>
            <TabsTrigger value="consensus">Konsensüs</TabsTrigger>
          </TabsList>
          
          <TabsContent value="evidence" className="flex-1">
            <EvidencePanel caseId={id} />
          </TabsContent>
          
          <TabsContent value="timeline" className="flex-1">
            <Timeline caseId={id} granularity="month" />
          </TabsContent>
          
          <TabsContent value="consensus" className="flex-1">
            <ConsensusPanel caseId={id} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
```

---

## 6. AI/ML Pipeline Implementation

### 6.1 Model Adapter Pattern

```python
# services/judge/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from schemas import JudgeOutput

class BaseJudge(ABC):
    """Abstract base class for model judges."""
    
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
    
    @abstractmethod
    async def analyze(
        self, 
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: list
    ) -> JudgeOutput:
        """Analyze evidence pack and return structured output."""
        pass
    
    @abstractmethod
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: list
    ) -> str:
        """Build model-specific prompt."""
        pass
    
    def _validate_output(self, output: Dict[str, Any]) -> JudgeOutput:
        """Validate and parse model output."""
        # JSON schema validation
        # Claim-evidence integrity check
        # Required field verification
        return JudgeOutput(**output)
```

### 6.2 Gemini Implementation

```python
# services/judge/gemini.py
import google.generativeai as genai
from services.judge.base import BaseJudge
from schemas import JudgeOutput

SYSTEM_PROMPT = """You are a historical analysis judge.
You must:
- Use ONLY the provided Evidence Pack.
- Produce structured JSON.
- No claim without at least one evidence reference.
- Distinguish discourse evidence from event evidence.
- Explicitly list uncertainties.
- Do not speculate beyond the evidence.

Output must follow this exact JSON schema:
{
  "definitions_review": [...],
  "claims": [...],
  "strongest_evidence": [...],
  "strongest_counter_evidence": [...],
  "uncertainties": [...],
  "bias_risk_notes": [...],
  "verdict": {...}
}"""

class GeminiJudge(BaseJudge):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-preview",
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.1,
                "response_mime_type": "application/json"
            }
        )
    
    async def analyze(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: list
    ) -> JudgeOutput:
        prompt = self._build_prompt(proposition, definitions, evidence_pack)
        
        try:
            response = await self.model.generate_content_async(
                prompt,
                timeout=self.timeout
            )
            
            output = json.loads(response.text)
            return self._validate_output(output)
            
        except TimeoutError:
            raise JudgeTimeoutError(f"Gemini timeout for case {case_id}")
        except json.JSONDecodeError as e:
            raise JudgeParseError(f"Invalid JSON from Gemini: {e}")
    
    def _build_prompt(
        self,
        proposition: str,
        definitions: Dict[str, Any],
        evidence_pack: list
    ) -> str:
        evidence_text = self._format_evidence_pack(evidence_pack)
        
        return f"""Analyze the following historical proposition:

PROPOSITION: {proposition}

OPERATIONAL DEFINITIONS: {json.dumps(definitions, indent=2)}

EVIDENCE PACK:
{evidence_text}

Provide your analysis in the required JSON format."""
    
    def _format_evidence_pack(self, evidence_pack: list) -> str:
        formatted = []
        for i, item in enumerate(evidence_pack, 1):
            formatted.append(f"""
EVIDENCE [{i}]:
- ID: {item['id']}
- Type: {item['source_type']}
- Reliability: {item['reliability_score']}
- Country/Language: {item['country']}/{item['language']}
- Text: {item['text'][:500]}...
""")
        return "\n".join(formatted)
```

### 6.3 Judge Orchestrator

```python
# services/judge/orchestrator.py
import asyncio
from typing import List, Dict
from services.judge.gemini import GeminiJudge
from services.judge.gpt import GPTJudge
from services.judge.claude import ClaudeJudge
from schemas import JudgeOutput, ConsensusInput

class JudgeOrchestrator:
    def __init__(self):
        self.judges = {
            'gemini': GeminiJudge(api_key=settings.GEMINI_API_KEY),
            'gpt': GPTJudge(api_key=settings.OPENAI_API_KEY),
            'claude': ClaudeJudge(api_key=settings.ANTHROPIC_API_KEY)
        }
    
    async def run_parallel_analysis(
        self,
        case_id: str,
        proposition: str,
        definitions: Dict,
        evidence_pack: List[Dict]
    ) -> Dict[str, JudgeOutput]:
        """Run all judges in parallel with timeout handling."""
        
        tasks = {
            name: self._run_with_timeout(
                judge, case_id, proposition, definitions, evidence_pack
            )
            for name, judge in self.judges.items()
        }
        
        # Execute all tasks concurrently
        results = await asyncio.gather(
            *tasks.values(),
            return_exceptions=True
        )
        
        # Process results
        outputs = {}
        for (name, _), result in zip(tasks.items(), results):
            if isinstance(result, Exception):
                # Log error, continue with partial consensus
                logger.error(f"Judge {name} failed: {result}")
                outputs[name] = None
            else:
                outputs[name] = result
        
        # Require at least 2 successful judges
        successful = sum(1 for o in outputs.values() if o is not None)
        if successful < 2:
            raise InsufficientConsensusError(
                f"Only {successful} judges succeeded, minimum 2 required"
            )
        
        return outputs
    
    async def _run_with_timeout(
        self,
        judge: BaseJudge,
        case_id: str,
        proposition: str,
        definitions: Dict,
        evidence_pack: List[Dict]
    ) -> JudgeOutput:
        """Run a single judge with timeout."""
        try:
            return await asyncio.wait_for(
                judge.analyze(case_id, proposition, definitions, evidence_pack),
                timeout=judge.timeout
            )
        except asyncio.TimeoutError:
            raise JudgeTimeoutError(f"Judge {judge.__class__.__name__} timed out")
```

### 6.4 Consensus Engine

```python
# services/consensus_engine.py
from typing import List, Dict, Set
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from schemas import Claim, ConsensusResult

class ConsensusEngine:
    SIMILARITY_THRESHOLD = 0.85
    
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
    
    async def compute_consensus(
        self,
        model_outputs: Dict[str, JudgeOutput]
    ) -> ConsensusResult:
        """Compute weighted consensus from multiple model outputs."""
        
        # Step 1: Extract and normalize all claims
        all_claims = []
        for model_name, output in model_outputs.items():
            if output:
                for claim in output.claims:
                    all_claims.append({
                        'model': model_name,
                        'claim': claim
                    })
        
        # Step 2: Group semantically similar claims
        claim_groups = await self._group_similar_claims(all_claims)
        
        # Step 3: Compute consensus for each group
        consensus_claims = []
        for group in claim_groups:
            consensus_claim = await self._compute_group_consensus(group)
            consensus_claims.append(consensus_claim)
        
        # Step 4: Categorize by confidence
        core_claims = [c for c in consensus_claims if c.confidence_label == 'high']
        medium_claims = [c for c in consensus_claims if c.confidence_label == 'medium']
        disputed_claims = [c for c in consensus_claims if c.is_disputed]
        
        # Step 5: Build agreement matrix
        agreement_matrix = self._build_agreement_matrix(
            model_outputs.keys(), 
            claim_groups
        )
        
        return ConsensusResult(
            core_claims=core_claims,
            medium_claims=medium_claims,
            disputed_claims=disputed_claims,
            agreement_matrix=agreement_matrix,
            overall_confidence=self._compute_overall_confidence(consensus_claims)
        )
    
    async def _group_similar_claims(
        self, 
        all_claims: List[Dict]
    ) -> List[List[Dict]]:
        """Group claims by semantic similarity."""
        
        # Generate embeddings for all claims
        texts = [c['claim'].normalized_text for c in all_claims]
        embeddings = await self.embedding_service.encode(texts)
        
        # Compute similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Group using connected components
        n = len(all_claims)
        visited = set()
        groups = []
        
        for i in range(n):
            if i in visited:
                continue
            
            # Find all similar claims
            group = [i]
            visited.add(i)
            
            for j in range(i + 1, n):
                if j not in visited and similarity_matrix[i][j] >= self.SIMILARITY_THRESHOLD:
                    group.append(j)
                    visited.add(j)
            
            groups.append([all_claims[idx] for idx in group])
        
        return groups
    
    async def _compute_group_consensus(self, group: List[Dict]) -> Claim:
        """Compute consensus for a group of similar claims."""
        
        # Aggregate evidence
        all_evidence = []
        for item in group:
            all_evidence.extend(item['claim'].evidence_refs)
        
        # Compute evidence strength
        evidence_strength = self._compute_evidence_strength(all_evidence)
        
        # Compute agreement ratio
        supporting_models = set(item['model'] for item in group)
        agreement_ratio = len(supporting_models) / 3  # Total models
        
        # Final score
        final_score = agreement_ratio * evidence_strength
        
        # Determine confidence label
        if final_score >= 0.61:
            confidence_label = 'high'
        elif final_score >= 0.31:
            confidence_label = 'medium'
        else:
            confidence_label = 'low'
        
        # Check if disputed
        stances = set(item['claim'].stance for item in group)
        is_disputed = len(stances) > 1
        
        return Claim(
            normalized_text=group[0]['claim'].normalized_text,
            category=group[0]['claim'].category,
            stance=self._majority_stance(group),
            evidence_refs=all_evidence,
            evidence_strength=evidence_strength,
            agreement_ratio=agreement_ratio,
            final_score=final_score,
            confidence_label=confidence_label,
            is_core_consensus=(confidence_label == 'high' and not is_disputed),
            is_disputed=is_disputed
        )
    
    def _compute_evidence_strength(self, evidence_refs: List[Dict]) -> float:
        """Compute weighted evidence strength."""
        type_weights = {
            'primary': 1.0,
            'academic': 0.8,
            'secondary': 0.7,
            'memoir': 0.5,
            'press': 0.4
        }
        
        total_weight = 0
        for ref in evidence_refs:
            source_type = ref.get('source_type', 'press')
            reliability = ref.get('reliability', 0.5)
            weight = type_weights.get(source_type, 0.4) * reliability
            total_weight += weight
        
        # Normalize to 0-1 range (assuming max 10 evidence items)
        return min(total_weight / 10, 1.0)
    
    def _majority_stance(self, group: List[Dict]) -> str:
        """Determine majority stance in claim group."""
        stance_counts = {}
        for item in group:
            stance = item['claim'].stance
            stance_counts[stance] = stance_counts.get(stance, 0) + 1
        return max(stance_counts, key=stance_counts.get)
```

---

## 7. Deployment Strategy

### 7.1 Docker Configuration

```dockerfile
# apps/api/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production image
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY app/ ./app/

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# apps/web/Dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
RUN mkdir .next
RUN chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### 7.2 Docker Compose (Local Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/polyhistory
      - REDIS_URL=redis://redis:6379/0
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./apps/api/app:/app/app
    depends_on:
      - db
      - redis
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  web:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - API_URL=http://api:8000
    volumes:
      - ./apps/web:/app
      - /app/node_modules
    depends_on:
      - api
    command: npm run dev

  db:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=polyhistory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/polyhistory
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: celery -A app.tasks worker --loglevel=info

  celery-beat:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/polyhistory
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: celery -A app.tasks beat --loglevel=info

volumes:
  postgres_data:
```

### 7.3 Kubernetes Deployment (Production)

```yaml
# infrastructure/k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: polyhistory-api
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: polyhistory-api
  template:
    metadata:
      labels:
        app: polyhistory-api
    spec:
      containers:
      - name: api
        image: polyhistory/api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: polyhistory-api
  namespace: production
spec:
  selector:
    app: polyhistory-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### 7.4 CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-api:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_polyhistory
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        working-directory: ./apps/api
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt

      - name: Run tests
        working-directory: ./apps/api
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_polyhistory
          REDIS_URL: redis://localhost:6379/0
        run: pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./apps/api/coverage.xml

  test-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: ./apps/web/package-lock.json

      - name: Install dependencies
        working-directory: ./apps/web
        run: npm ci

      - name: Lint
        working-directory: ./apps/web
        run: npm run lint

      - name: Type check
        working-directory: ./apps/web
        run: npm run type-check

      - name: Test
        working-directory: ./apps/web
        run: npm run test:ci

  build:
    needs: [test-api, test-web]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push API
        uses: docker/build-push-action@v5
        with:
          context: ./apps/api
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/api:${{ github.sha }}
            ghcr.io/${{ github.repository }}/api:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push Web
        uses: docker/build-push-action@v5
        with:
          context: ./apps/web
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/web:${{ github.sha }}
            ghcr.io/${{ github.repository }}/web:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 8. Testing Strategy

### 8.1 Backend Testing

```python
# tests/test_consensus_engine.py
import pytest
from unittest.mock import Mock, AsyncMock
from services.consensus_engine import ConsensusEngine

@pytest.fixture
def embedding_service():
    service = Mock()
    service.encode = AsyncMock(return_value=[
        [0.1, 0.2, 0.3],
        [0.11, 0.21, 0.31],  # Similar to first
        [0.9, 0.8, 0.7]      # Different
    ])
    return service

@pytest.fixture
def consensus_engine(embedding_service):
    return ConsensusEngine(embedding_service)

@pytest.mark.asyncio
async def test_group_similar_claims(consensus_engine):
    claims = [
        {'claim': Mock(normalized_text='Claim A')},
        {'claim': Mock(normalized_text='Claim A similar')},
        {'claim': Mock(normalized_text='Completely different claim')}
    ]
    
    groups = await consensus_engine._group_similar_claims(claims)
    
    assert len(groups) == 2
    assert len(groups[0]) == 2  # First two grouped together
    assert len(groups[1]) == 1  # Third separate

@pytest.mark.asyncio
async def test_compute_evidence_strength(consensus_engine):
    evidence = [
        {'source_type': 'primary', 'reliability': 0.9},
        {'source_type': 'press', 'reliability': 0.5}
    ]
    
    strength = consensus_engine._compute_evidence_strength(evidence)
    
    # Primary: 1.0 * 0.9 = 0.9
    # Press: 0.4 * 0.5 = 0.2
    # Total: 1.1 / 10 = 0.11
    expected = (1.0 * 0.9 + 0.4 * 0.5) / 10
    assert abs(strength - expected) < 0.001
```

### 8.2 Frontend Testing

```typescript
// components/__tests__/evidence-panel.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { EvidencePanel } from '../evidence/evidence-panel'
import { useEvidenceStore } from '@/stores/evidence-store'

jest.mock('@/stores/evidence-store')

describe('EvidencePanel', () => {
  const mockEvidence = [
    {
      id: '1',
      title: 'Test Evidence',
      source_type: 'primary',
      country: 'TR',
      language: 'tr',
      reliability_score: 0.9,
      stance: 'pro'
    }
  ]

  beforeEach(() => {
    (useEvidenceStore as jest.Mock).mockReturnValue({
      evidence: mockEvidence,
      isLoading: false
    })
  })

  it('renders evidence items', () => {
    render(<EvidencePanel caseId="test-123" />)
    expect(screen.getByText('Test Evidence')).toBeInTheDocument()
  })

  it('filters by source type', () => {
    render(<EvidencePanel caseId="test-123" />)
    
    const filterSelect = screen.getByLabelText('Kaynak Türü')
    fireEvent.change(filterSelect, { target: { value: 'press' } })
    
    expect(screen.queryByText('Test Evidence')).not.toBeInTheDocument()
  })
})
```

### 8.3 Integration Testing

```python
# tests/integration/test_case_workflow.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_end_to_end_case_workflow(client: AsyncClient):
    # 1. Create case
    response = await client.post('/api/v1/cases', json={
        'proposition': 'Test historical claim',
        'time_window': {'start': '1920-01-01', 'end': '1923-12-31'},
        'options': {
            'languages': ['tr', 'en']
        }
    })
    assert response.status_code == 201
    case_id = response.json()['id']
    
    # 2. Check initial status
    response = await client.get(f'/api/v1/cases/{case_id}')
    assert response.json()['status'] == 'processing'
    
    # 3. Wait for completion (poll with timeout)
    for _ in range(30):
        response = await client.get(f'/api/v1/cases/{case_id}')
        if response.json()['status'] == 'completed':
            break
        await asyncio.sleep(1)
    
    # 4. Verify results
    assert response.json()['status'] == 'completed'
    assert 'verdict' in response.json()
    assert response.json()['mbr_compliant'] is True
    
    # 5. Check evidence
    response = await client.get(f'/api/v1/cases/{case_id}/evidence')
    evidence = response.json()
    assert len(evidence) > 0
    
    # 6. Check consensus
    response = await client.get(f'/api/v1/cases/{case_id}/consensus')
    consensus = response.json()
    assert 'core_claims' in consensus
```

### 8.4 E2E Testing

```typescript
// e2e/case-creation.spec.ts
import { test, expect } from '@playwright/test'

test('user can create and view a case', async ({ page }) => {
  // Login
  await page.goto('/auth/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password123')
  await page.click('button[type="submit"]')
  
  // Create new case
  await page.click('text=Yeni Analiz')
  await page.fill('[name="proposition"]', 'Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?')
  await page.fill('[name="startDate"]', '1919-05-01')
  await page.fill('[name="endDate"]', '1923-10-29')
  await page.click('text=Analiz Başlat')
  
  // Wait for processing
  await expect(page.locator('text=Analiz tamamlandı')).toBeVisible({ timeout: 60000 })
  
  // Verify evidence panel
  await page.click('text=Kanıtlar')
  await expect(page.locator('.evidence-card')).toHaveCount.greaterThan(0)
  
  // Verify timeline
  await page.click('text=Zaman Çizelgesi')
  await expect(page.locator('svg')).toBeVisible()
})
```

---

## 9. Development Timeline

### 9.1 MVP Sprint Planning (Weeks 1-4)

#### Sprint 1: Foundation (Days 1-7)

**Day 1-2: Project Setup**
- [ ] Initialize monorepo structure
- [ ] Set up Docker Compose for local development
- [ ] Configure CI/CD pipeline skeleton
- [ ] Set up PostgreSQL + pgvector
- [ ] Set up Redis

**Day 3-4: Database & Models**
- [ ] Create SQLAlchemy models
- [ ] Create initial Alembic migrations
- [ ] Create Pydantic schemas
- [ ] Implement base repository pattern

**Day 5-7: Core API**
- [ ] FastAPI app structure
- [ ] Authentication endpoints (JWT)
- [ ] Case CRUD endpoints
- [ ] Basic error handling

**Deliverable:** Working API with auth and case management

#### Sprint 2: Retrieval & Evidence (Days 8-14)

**Day 8-9: Text Processing**
- [ ] PDF/text extraction service
- [ ] OCR integration (Tesseract)
- [ ] Language detection
- [ ] Text chunking with semantic boundaries

**Day 10-11: Embedding Pipeline**
- [ ] Sentence transformers integration
- [ ] Embedding generation service
- [ ] Vector storage in pgvector
- [ ] Similarity search endpoint

**Day 12-13: Evidence Builder**
- [ ] Source classification logic
- [ ] Reliability scoring algorithm
- [ ] Snippet extraction
- [ ] Evidence Pack assembly

**Day 14: Retrieval Collectors**
- [ ] Academic collector (Semantic Scholar API)
- [ ] Basic press collector
- [ ] Query expansion (basic)

**Deliverable:** Evidence pipeline working end-to-end

#### Sprint 3: AI Integration (Days 15-21)

**Day 15-16: Model Adapters**
- [ ] Gemini adapter implementation
- [ ] GPT adapter implementation
- [ ] Claude adapter implementation
- [ ] Base judge class abstraction

**Day 17-18: Judge Orchestrator**
- [ ] Parallel execution logic
- [ ] Timeout handling
- [ ] Error fallback strategies
- [ ] Model output validation

**Day 19-20: Consensus Engine**
- [ ] Claim normalization
- [ ] Semantic similarity grouping
- [ ] Evidence strength calculation
- [ ] Agreement score computation
- [ ] Confidence labeling

**Day 21: Balance Protocol**
- [ ] MBR validation logic
- [ ] Source clustering checks
- [ ] High-risk claim detection
- [ ] Penalty application

**Deliverable:** Multi-model analysis with consensus

#### Sprint 4: Frontend & Polish (Days 22-28)

**Day 22-23: Frontend Setup**
- [ ] Next.js project setup
- [ ] shadcn/ui configuration
- [ ] API client setup (React Query)
- [ ] Zustand stores

**Day 24-25: Core UI Components**
- [ ] Chat interface
- [ ] Case creation form
- [ ] Evidence panel
- [ ] Case list/dashboard

**Day 26: Visualization**
- [ ] Timeline component (D3.js)
- [ ] Consensus panel
- [ ] Agreement heatmap
- [ ] Source distribution charts

**Day 27: Export & Polish**
- [ ] Markdown export
- [ ] PDF export
- [ ] Loading states
- [ ] Error handling
- [ ] Responsive design

**Day 28: Testing & Documentation**
- [ ] Integration tests
- [ ] API documentation
- [ ] README updates
- [ ] Deployment preparation

**Deliverable:** MVP complete and deployed

### 9.2 Post-MVP Sprints (Months 2-3)

#### Sprint 5: Enhancement (Week 5-6)
- [ ] FR + EL language support
- [ ] Advanced query expansion
- [ ] NLI contradiction detection
- [ ] Archive connector framework

#### Sprint 6: Scale & Optimize (Week 7-8)
- [ ] Performance optimization
- [ ] Caching layer improvements
- [ ] Rate limiting refinement
- [ ] Monitoring & alerting

#### Sprint 7: B2B Features (Week 9-10)
- [ ] API key management
- [ ] Usage analytics dashboard
- [ ] Bulk case operations
- [ ] Team/organization support

#### Sprint 8: Launch Prep (Week 11-12)
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation completion
- [ ] Marketing site

---

## 10. Resource Requirements

### 10.1 Team Structure

| Role | Count | Duration | Responsibilities |
|------|-------|----------|------------------|
| Tech Lead / Architect | 1 | Full project | Architecture, code review, DevOps |
| Backend Engineer | 2 | MVP + 3 months | API, AI pipeline, data layer |
| Frontend Engineer | 1 | MVP + 3 months | Next.js UI, visualization |
| ML Engineer | 1 | MVP + 2 months | Model adapters, consensus engine |
| DevOps Engineer | 0.5 | Month 2 onwards | Infrastructure, CI/CD, monitoring |
| QA Engineer | 0.5 | Month 2 onwards | Testing, automation |

### 10.2 Infrastructure Costs (Monthly)

| Component | Provider | Estimated Cost |
|-----------|----------|----------------|
| Compute (K8s) | AWS/GCP | $500-800 |
| PostgreSQL (Managed) | AWS RDS / Cloud SQL | $200-400 |
| Redis | AWS ElastiCache | $50-100 |
| Vector DB | pgvector (self-hosted) | $0 (included) |
| Object Storage | S3 / GCS | $50-100 |
| CDN | CloudFront / CloudFlare | $50-100 |
| Monitoring | Datadog / Grafana Cloud | $100-200 |
| AI APIs | OpenAI, Google, Anthropic | $500-2000 (usage-based) |
| **Total** | | **$1,450-3,700/month** |

### 10.3 Third-Party Services

| Service | Purpose | Cost |
|---------|---------|------|
| OpenAI API | GPT-4/3.5 | Usage-based |
| Google AI | Gemini Pro | Usage-based |
| Anthropic | Claude | Usage-based |
| Semantic Scholar | Academic papers | Free tier |
| SerpAPI | Search results | $50-200/mo |
| Cloudflare | DNS, security | $20/mo |
| GitHub | Repos, Actions | $50/mo |
| Figma | Design | $15/mo |
| Notion | Documentation | $10/mo |

---

## 11. Risk Mitigation

### 11.1 Technical Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Model API rate limits | High | Implement caching, queue management, graceful degradation |
| Slow vector search | Medium | Proper indexing (HNSW), query optimization, scaling |
| Data quality issues | High | Reliability scoring, OCR confidence, manual review workflow |
| Celery task failures | Medium | Dead letter queues, retry logic, monitoring alerts |

### 11.2 Timeline Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Integration complexity | Medium | Parallel development streams, early integration testing |
| Scope creep | High | Strict MVP definition, feature freeze, prioritization |
| Team availability | Medium | Cross-training, documentation, contractor backup |

### 11.3 Contingency Plans

**If model consensus is unreliable:**
- Fallback to 2-model agreement
- Increase evidence threshold
- Add human-in-the-loop review

**If retrieval is too slow:**
- Implement aggressive caching
- Limit initial source count
- Background pre-fetching

**If costs exceed budget:**
- Implement stricter rate limiting
- Tiered source access
- Optimize token usage

---

## 12. Success Criteria

### 12.1 MVP Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Case creation to completion | <60 seconds | Backend logging |
| MBR compliance rate | >80% | Database query |
| Model consensus rate | >70% | Consensus logs |
| API error rate | <1% | Error tracking |
| UI load time | <3s | Lighthouse |
| Test coverage | >70% | Coverage reports |

### 12.2 Launch Readiness Checklist

- [ ] All critical paths tested
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Monitoring configured
- [ ] Rollback plan ready
- [ ] Support channels established

---

*End of Implementation Plan*
