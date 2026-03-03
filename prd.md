# Product Requirements Document (PRD)
## PolyHistory: Evidence-First Multi-Perspective Historical Analysis Platform

**Version:** 2.0  
**Date:** March 3, 2026  
**Status:** Final Draft  
**Prepared by:** Product Team  

---

## 1. Executive Summary

### 1.1 Product Overview
PolyHistory is an AI-powered historical research and analysis platform designed to provide evidence-based, multi-perspective, and cross-national historical discourse analysis. The platform addresses the critical problem of ideological echo chambers in historical research by enforcing strict source diversity, hierarchical evidence weighting, and multi-model consensus mechanisms.

### 1.2 Core Value Proposition
> "Aynı tarih aralığında, farklı ülkelerin ve farklı görüşlerin ne dediğini önce göster; sonra kanıt hiyerarşisine göre, denetlenebilir bir çıkarım üret."

### 1.3 Key Differentiators
- **Evidence-First Architecture:** No claim without citation enforcement
- **Multi-Model Consensus:** Three independent AI judges (Gemini, GPT, Claude) with weighted agreement scoring
- **Minimum Balance Requirements (MBR):** Mandatory source diversity across perspectives and geographies
- **Same-Time-Window Analysis:** Synchronized cross-national discourse mapping
- **Auditability:** Complete case files with deterministic replay capability

---

## 2. Problem Statement

### 2.1 Current Pain Points
1. **Ideological Echo Chambers:** Users are exposed to single-perspective historical narratives
2. **Source Conflation:** No distinction between primary archives, academic peer-review, and press discourse
3. **Cross-National Blindspots:** Inability to compare how different countries reported the same events simultaneously
4. **Hallucination Risks:** AI systems generating claims without verifiable evidence
5. **Lack of Transparency:** Opaque reasoning chains and hidden biases

### 2.2 Target Impact
Reduce ideological bias in historical discourse while increasing transparency, traceability, and academic rigor in AI-assisted historical research.

---

## 3. Product Vision & Objectives

### 3.1 Vision Statement
To establish the global standard for evidence-based historical analysis by creating an AI system that prioritizes source hierarchy, enforces perspective diversity, and provides auditable reasoning chains.

### 3.2 Strategic Objectives

| Objective | Success Metric | Timeline |
|-----------|---------------|----------|
| Launch MVP (Internal Alpha) | Functional end-to-end pipeline | Month 1 |
| Turkey Beta Launch | 500 beta users, advisory board formed | Month 4 |
| Establish academic credibility | 5 university partnerships | Month 6 |
| Turkey GA + English Beta | 5,000 MAU (TR), US/UK pilot programs | Month 9 |
| English GA + Profitability | Positive unit economics, 25,000 MAU | Month 12 |
| European Expansion | FR/DE/EL support, 10 institutional partnerships | Month 18 |

### 3.3 Non-Negotiable Principles
1. **No Citation, No Claim:** Every assertion must link to specific evidence
2. **Minimum Balance Requirements:** Mandatory source diversity
3. **Steel-man Principle:** Present the strongest counter-argument before conclusions
4. **Uncertainty Transparency:** Explicit disclosure of gaps and limitations
5. **Auditability:** Complete traceability from query to conclusion

---

## 4. Target Audience & Personas

### 4.1 Primary Personas

#### 4.1.1 Academic Researcher - "Dr. Ayşe"
- **Demographics:** History PhD candidate, age 28, Istanbul
- **Goals:** Cross-reference Ottoman archives with European diplomatic records
- **Pain Points:** Language barriers, source verification time, access to foreign archives
- **Usage Pattern:** Research Tier subscriber, bulk case generation, citation exports

#### 4.1.2 Investigative Journalist - "Mehmet"
- **Demographics:** Political reporter, age 35, Ankara
- **Goals:** Fact-check historical claims in current political discourse
- **Pain Points:** Time pressure, verification complexity, bias accusations
- **Usage Pattern:** Pro Tier, timeline analysis, quick confidence assessment

#### 4.1.3 Content Creator - "HistoryChannel_TR"
- **Demographics:** YouTube historian, age 32, Izmir
- **Goals:** Create evidence-based content with credible sources
- **Pain Points:** Finding diverse perspectives, audience trust, source visualization
- **Usage Pattern:** Pro Tier, evidence panel screenshots, timeline exports

### 4.2 Secondary Personas
- Policy Researchers at think-tanks
- High school history teachers
- Museum curators and archivists
- Legal professionals (historical precedent research)

### 4.3 Geographic Strategy

#### Phase 1: Turkey — MVP & Beta (Months 1-6)
- Target: University history departments, journalists, content creators
- Positioning: "Çok Kaynaklı Tarih Analiz Platformu" (Non-political)
- Languages: TR, EN (core), Ottoman Turkish OCR (beta)

#### Phase 2: Turkey GA + English Beta (Months 7-9)
- Target: US/UK academic institutions, policy research institutes
- Positioning: "Evidence-first historical analysis engine"
- Languages: Full EN support

#### Phase 3: English GA + European Expansion (Months 10-18)
- Target: European diplomatic history researchers, think-tanks
- Languages: FR, DE, EL full support

#### Phase 4: MENA & Eurasia (Months 18-24)
- Target: Middle Eastern and Russian-language historical research communities
- Languages: AR, RU full support
- Focus: Ottoman provincial archives, Russian diplomatic records

---

## 5. Functional Requirements

### 5.1 User Interface Requirements

#### 5.1.1 Chat Interface (FR-UI-001)
- **Description:** Primary interaction interface for query input and response display
- **Acceptance Criteria:**
  - Streaming response capability
  - Rich text support with inline citations
  - Collapsible evidence panels
  - Query history persistence
  - Export options (Markdown, PDF, JSON)

#### 5.1.2 Advanced Query Builder (FR-UI-002)
- **Description:** Structured input for complex research queries
- **Fields:**
  - Natural language proposition input
  - Date range selector (with auto-suggestion)
  - Geography multi-select
  - Source type weight preference (Primary-only / Balanced / Broad)
  - Language scope (TR/EN/FR/EL)
  - Steelman requirement toggle (default: ON)

#### 5.1.3 Evidence Explorer Panel (FR-UI-003)
- **Description:** Interactive source browser with filtering
- **Features:**
  - Source list with reliability scores
  - Country/language filters
  - Type filters (primary/secondary/press/memoir)
  - Snippet viewer with page/paragraph references
  - Cross-reference highlighting
  - Bibliography export (APA/Chicago)

#### 5.1.4 Timeline Visualization (FR-UI-004)
- **Description:** Chronological event and discourse mapping
- **Features:**
  - Zoom capability (year/month/week/day)
  - Multi-track display (TR pro/ TR contra / UK / FR / GR)
  - Event markers with source links
  - Synchronized scrolling
  - Export as image/PDF

#### 5.1.5 Disagreement Analysis Panel (FR-UI-005)
- **Description:** Visualization of model consensus and divergence
- **Features:**
  - Agreement heatmap
  - Claim-by-claim comparison
  - Disagreement classification (definition/evidence/time/translation)
  - Model-specific reasoning display

### 5.2 Backend System Requirements

#### 5.2.1 Proposition Parser Service (FR-BE-001)
- **Description:** NLP service for structured proposition extraction
- **Inputs:** Natural language query
- **Outputs:**
  ```json
  {
    "entities": ["Mustafa Kemal", "İngiltere"],
    "time_window": {"start": "1919-05-01", "end": "1923-10-29"},
    "geography": ["Turkey", "UK"],
    "claim_type": "diplomatic|economic|military|intelligence|propaganda",
    "ambiguity_terms": ["iş yapmak"],
    "normalized_definitions": {
      "iş yapmak": ["diplomatic_contact", "economic_agreement", "intelligence_cooperation"]
    }
  }
  ```
- **Requirements:**
  - Named Entity Recognition (NER) for historical figures and locations
  - Temporal inference with default suggestions
  - Concept disambiguation
  - Query seed generation for retrieval

#### 5.2.2 Multi-Lingual Query Expansion Engine (FR-BE-002)
- **Description:** Generate language-specific query variations
- **Supported Languages:**
  - Phase 1 (Months 1-6): TR, EN
  - Phase 2 (Months 7-9): Ottoman Turkish (transliterated)
  - Phase 3 (Months 10-18): FR, DE, EL
  - Phase 4 (Months 18-24): AR, RU
- **Capabilities:**
  - Period terminology mapping (e.g., "Angora Government" ↔ "Ankara Government")
  - Actor name variants (e.g., "Mustafa Kemal" ↔ "Kemal Pasha" ↔ "مصطفى كمال")
  - Institution and location mappings (historical ↔ modern names)
  - Keyword clustering (treaty, correspondence, dispatch, communiqué)
  - Ottoman Turkish ↔ Modern Turkish transliteration

#### 5.2.3 Retrieval Cluster (FR-BE-003)
- **Sub-components:**
  - **Academic Collector:** Article metadata, open-access PDFs, bibliographic records
  - **Archive Collector:** Catalog queries, document reference numbers
  - **Press Collector:** Period newspapers, magazine archives
  - **Treaty/Official Text Collector:** Agreement texts, parliamentary records, diplomatic correspondence indices
- **Target Data Sources (Phase 1):**
  - **Turkey:** T.C. Cumhurbaşkanlığı Devlet Arşivleri (BOA/BCA), TBMM Tutanakları, İSAM Kütüphanesi
  - **UK:** The National Archives (PRO/Kew) — FO 371/406 series, Hansard Parliamentary Records
  - **France:** Archives diplomatiques (La Courneuve), Gallica BnF
  - **Academic:** JSTOR, Google Scholar, OpenAlex, Semantic Scholar
  - **Press:** Hathi Trust, Chronicling America, Türk Basın Arşivi
- **Access Strategy:**
  - API-first for sources with public APIs (Google Scholar, OpenAlex, Semantic Scholar)
  - Licensed access agreements for institutional archives
  - Web scraping with politeness protocols for open-access catalogs
  - OCR pipeline for scanned/digitized documents
- **Requirements:**
  - Rate limiting and politeness protocols
  - Caching layer for frequent queries (Redis, TTL: 24h)
  - Source reliability pre-scoring
  - Retry with exponential backoff for failed retrievals

#### 5.2.4 Text Processing Pipeline (FR-BE-004)
- **Stages:**
  1. Document fetch with retry logic
  2. Format detection (digital text / scanned image / mixed)
  3. OCR processing (when needed) with confidence scoring
     - Modern Latin script OCR (Tesseract / Azure Document Intelligence)
     - **Ottoman Turkish OCR** (Arabic-script, specialized model)
     - Confidence threshold: ≥ 0.70 to proceed; below triggers manual review flag
  4. Ottoman Turkish → Modern Turkish transliteration (when applicable)
  5. Language detection
  6. Text normalization and cleaning
  7. Semantic chunking (target: 512 tokens with 64-token overlap)
  8. Embedding generation (Sentence Transformers)
  9. Metadata enrichment (author, date, institution, geography, source type)
- **Output Schema per Chunk:**
  ```json
  {
    "source_id": "uuid",
    "language": "tr",
    "page_location": "p.45, para.3",
    "semantic_vector": [0.1, 0.2, ...],
    "quality_score": 0.92,
    "text": "..."
  }
  ```

#### 5.2.5 Evidence Builder (FR-BE-005)
- **Description:** Assemble Evidence Pack from processed documents
- **Functionality:**
  - Relevant chunk selection via semantic similarity
  - Source classification (primary/secondary/press/memoir)
  - Reliability scoring algorithm
  - Snippet extraction with context preservation
  - Cross-reference detection
- **Reliability Score Formula:**
  > All component values are normalized to [0.0, 1.0] range. Final score is also [0.0, 1.0].
  ```
  Reliability = (Source_Type_Score × 0.35) + 
                (Institution_Reputation × 0.25) + 
                (Citation_Density × 0.15) + 
                (Cross_Source_Consistency × 0.15) + 
                (Document_Quality × 0.10)
  ```
  - **Source_Type_Score:** Primary archive = 1.0, Academic peer-reviewed = 0.85, Official/treaty = 0.80, Press = 0.60, Memoir = 0.50, Unverified = 0.20
  - **Document_Quality:** For OCR documents = OCR_Confidence; for born-digital = 1.0
  - **Cross_Source_Consistency:** Calculated iteratively — initial pass uses uniform priors, then refines over 2-3 iterations until convergence (Δ < 0.01)

#### 5.2.6 Multi-Model Judge Layer (FR-BE-006)
- **Models:**
  - Gemini 3.1 Pro Preview (broad context synthesis)
  - GPT-5.2 xhigh (claim decomposition, consistency checking)
  - Claude Opus 4.6 (steel-man argumentation, nuanced interpretation)
- **Requirements:**
  - Async parallel execution
  - Timeout handling: 30s per model, fallback to remaining models
  - Strict JSON output validation (retry up to 2× on schema failure)
  - Claim-to-evidence referential integrity
  - **Graceful Degradation Rules:**
    - 3/3 models respond → full consensus
    - 2/3 models respond → partial consensus + "reduced confidence" annotation
    - 1/3 models respond → single-model output + "no consensus" warning
    - 0/3 models respond → circuit breaker triggers, user notified, retry queued

#### 5.2.7 Consensus Engine (FR-BE-007)
- **Claim Graph Construction:**
  - Semantic similarity matching (threshold: ≥0.85)
  - Claim merging and normalization
  - Graph node creation per normalized claim
- **Evidence Aggregation:**
  > All scores normalized to [0.0, 1.0] before aggregation.
  ```
  Evidence_Strength = Σ(Source_Type_Score × Reliability_Score) / N_sources
  ```
  - Normalized by source count to prevent bias toward topics with more available sources
- **Agreement Score:**
  ```
  Agreement_Ratio = Supporting_Models / Responding_Models
  ```
  - Uses `Responding_Models` (not `Total_Models`) to handle graceful degradation
- **Final Claim Score:**
  ```
  Final_Claim_Score = (Agreement_Ratio × 0.4) + (Evidence_Strength × 0.6)
  ```
  - Evidence strength weighted higher than model agreement — strong evidence with model disagreement still produces meaningful scores, but triggers a "disputed" flag
- **Confidence Labels:**
  - Low: 0.00–0.30 → "Insufficient evidence or significant disagreement"
  - Medium: 0.31–0.60 → "Partial evidence with moderate support"
  - High: 0.61–0.85 → "Well-supported with broad agreement"
  - Very High: 0.86–1.00 → "Strong consensus with robust evidence"

#### 5.2.8 Balance Protocol Enforcement (FR-BE-008)
- **Minimum Balance Requirements (MBR):**
  - TR_sources ≥ 2
  - Foreign_countries ≥ 1 (≥ 2 preferred, adaptive based on topic scope)
  - Pro_stance_sources ≥ 1
  - Contra_stance_sources ≥ 1
- **Adaptive MBR Logic:**
  - If topic involves only 2 countries → Foreign_countries minimum = 1
  - If topic is domestic-only → Foreign sources become "recommended" not "required"
  - System auto-detects topic scope from Proposition Parser output
- **Source Cluster Minimums:**
  - Turkey: ≥1 primary/academic + ≥1 press
  - Foreign: ≥1 press + ≥1 official/academic
- **Enforcement Actions (if MBR not met):**
  1. Confidence score penalty: × 0.80 (multiplicative, prevents negative scores)
  2. Verdict annotation: "Balance requirement not fully satisfied — [missing clusters listed]"
  3. UI warning with missing cluster listing and suggested search terms
  4. Analysis still proceeds (never blocks) — user can override with acknowledgment

#### 5.2.9 High-Risk Claim Detection (FR-BE-009)
- **Trigger Keywords:** İşbirliği, ihanet, gizli anlaşma, casusluk, entrika
- **Rules:**
  - If primary evidence is absent: confidence cap = 60%
  - If only discourse evidence exists: claim category = propaganda
  - Event claims prohibited without event evidence

#### 5.2.10 Report Generator (FR-BE-010)
- **Output Formats:**
  - Structured JSON (UI consumption)
  - Markdown (human-readable)
  - PDF (formatted report)
  - Academic citation formats (APA, Chicago)
- **Report Sections:**
  1. Short verdict (2-6 sentences)
  2. Concept definitions (operational)
  3. Time-aligned discourse map
  4. Evidence ledger (strongest for/against)
  5. Official texts/agreements summary
  6. Steel-man counter-argument
  7. Uncertainties and data gaps
  8. Bibliography by cluster

### 5.3 Data Storage Requirements

#### 5.3.1 Evidence Store (FR-DB-001)
- **Document DB (PostgreSQL):**
  - Metadata, snippets, reliability scores
  - Country/language tags
  - Versioning support
- **Vector DB (Pinecone/Weaviate/pgvector):**
  - Semantic search capability
  - Claim-evidence vector mapping
  - Similarity query performance <100ms

#### 5.3.2 Case File Versioning (FR-DB-002)
- Every query generates a unique Case ID
- Evidence Pack snapshots stored immutably
- Model outputs archived
- Consensus computation logs preserved
- Deterministic replay capability

### 5.4 API Requirements

#### 5.4.1 Core Endpoints

**POST /api/v1/cases**
- Create new analysis case
- Body: proposition, time_window, options
- Response: case_id, status

**GET /api/v1/cases/{case_id}**
- Retrieve case results
- Response: full report object

**GET /api/v1/cases/{case_id}/evidence**
- Retrieve evidence pack
- Query params: source_type, country, language

**GET /api/v1/cases/{case_id}/timeline**
- Retrieve timeline data
- Query params: granularity, tracks

**GET /api/v1/cases/{case_id}/consensus**
- Retrieve consensus analysis
- Includes agreement matrix and disputed claims

**POST /api/v1/cases/{case_id}/export**
- Export case in specified format
- Body: format (markdown, pdf, json)

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

| Metric | Requirement | Measurement |
|--------|-------------|-------------|
| API Response Time (P95) | <500ms for case creation | New Relic/Datadog |
| Evidence Retrieval Time | <3 seconds per source | Internal logging |
| Model Judge Latency | <15 seconds per model | Model adapter logs |
| End-to-End Processing | <60 seconds for MVP | Case completion time |
| Concurrent Users | 1000 simultaneous | Load testing |
| Vector Search Latency | <100ms | Database metrics |

### 6.2 Scalability Requirements
- Horizontal scaling for retrieval cluster
- Async job queue (Celery/RabbitMQ) for model processing
- CDN for static assets and document caching
- Database read replicas for evidence queries

### 6.3 Security Requirements

#### 6.3.1 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Free/Pro/Research/Enterprise)
- API key management for B2B integrations

#### 6.3.2 Data Protection
- All user cases private by default
- GDPR compliance (right to deletion, data portability)
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)

#### 6.3.3 Input Validation
- Strict schema validation for all inputs
- SQL injection prevention
- XSS protection
- Rate limiting per user/IP

### 6.4 Reliability Requirements
- 99.9% uptime SLA for Pro/Research tiers
- 99.5% uptime target for Free tier
- Automated backup (daily snapshots, 30-day retention)
- Graceful degradation (partial results if one model fails — see FR-BE-006)
- Circuit breaker pattern for external APIs (threshold: 5 consecutive failures)
- Dead letter queue for failed case processing with automatic retry

### 6.5 Accessibility Requirements
- WCAG 2.1 AA compliance across all UI components
- Screen reader compatibility for evidence panels and reports
- Full keyboard navigation support
- Color contrast ratio ≥ 4.5:1 for all text elements
- Alternative text-based representations for:
  - Timeline visualizations (tabular event list)
  - Agreement heatmaps (structured data table)
  - Disagreement panels (claim-by-claim text comparison)
- Reduced motion mode for animations
- Aria labels on all interactive elements

### 6.6 Auditability Requirements
- Complete audit trail for every case
- Immutable case file storage
- Model output versioning
- Consensus computation logging
- User action logging (who queried what, when)

---

## 7. Monetization Strategy

### 7.1 Pricing Tiers

#### Free Tier
- **Price:** $0
- **Limits:**
  - 5 analyses per month total:
    - **1 full multi-model consensus analysis** (so users experience the core value)
    - 4 single-model analyses
  - Limited source visibility (top 10 sources)
  - No PDF export
  - Basic timeline only
  - Case archive: 10 cases (oldest auto-archived after 30 days)
- **Goal:** User acquisition, demonstrate multi-model value, drive conversion

#### Pro Tier
- **Price:** $19-39/month
- **Features:**
  - Unlimited analyses
  - Multi-model consensus
  - Full evidence panel access
  - Timeline + disagreement panel
  - PDF/Markdown export
  - Case file archive (100 cases)
  - Priority support
- **Target:** Academics, journalists, content creators

#### Research Tier
- **Price:** $79-149/month
- **Features:**
  - Everything in Pro
  - Custom time-window controls
  - Source weighting override
  - Advanced citation formats
  - Bulk case generation (up to 50)
  - Limited API access (1000 calls/month)
  - Case file archive (unlimited)
- **Target:** Research institutions, PhD candidates

#### Enterprise Tier
- **Price:** Custom pricing
- **Features:**
  - On-premise deployment option
  - Custom archive integrations
  - White-label reporting
  - Dedicated support
  - SLA guarantees
  - Unlimited API access
- **Target:** Media organizations, universities, think-tanks

### 7.2 B2B Offerings

#### Media Organizations
- Fact-checking integration
- Pre-publication verification API
- Editorial workflow integration

#### Universities
- Campus-wide licenses
- Educational discounts (50% off)
- Curriculum integration support
- Student usage analytics

#### Research Institutions
- Custom data source integration
- Advanced archive connectors
- Collaborative research features
- API-first access

### 7.3 Additional Revenue Streams
- **Custom Research Services:** $500-5000 per specialized case
- **Academic Reports:** White-label historical analysis reports
- **API Usage:** $0.01-0.05 per call beyond tier limits
- **Training & Workshops:** Institutional methodology training

### 7.4 Cost Projection & Unit Economics

#### Per-Query Cost Estimate (Full Multi-Model Analysis)

| Component | Estimated Cost | Notes |
|-----------|---------------|-------|
| Gemini 3.1 Pro Preview | ~$0.05-0.15 | Input/output token pricing |
| GPT-5.2 xhigh | ~$0.08-0.25 | Higher tier model |
| Claude Opus 4.6 | ~$0.06-0.20 | Depends on context length |
| Embedding generation | ~$0.01 | Sentence Transformers (self-hosted) |
| Vector DB query | ~$0.001 | Pinecone/pgvector |
| OCR processing | ~$0.01-0.05 | Only for scanned documents |
| Infrastructure overhead | ~$0.02 | Compute, storage, bandwidth |
| **Total per full analysis** | **~$0.23-0.68** | Varies by query complexity |

#### Monthly Cost Projections

| Scale | Users | Analyses/mo | Estimated Cost | Revenue Target |
|-------|-------|-------------|----------------|----------------|
| Alpha (M1-3) | 100 | 500 | ~$500 | $0 (pre-revenue) |
| Beta (M4-6) | 500 | 2,500 | ~$2,500 | ~$3,000 |
| Growth (M7-12) | 5,000 | 25,000 | ~$20,000 | ~$50,000 |
| Scale (M12+) | 25,000 | 125,000 | ~$80,000 | ~$200,000 |

#### Break-Even Analysis
- **Target gross margin:** ≥60%
- **Break-even point:** ~200 paid subscribers (Pro tier average)
- **Key cost levers:** Model API costs (negotiate volume discounts), caching hit rate (target ≥40%), single-model fallback for simple queries

### 7.5 API Versioning Strategy
- **Version format:** `/api/v{major}/` (e.g., `/api/v1/`, `/api/v2/`)
- **Backward compatibility:** Minimum 12-month support for deprecated API versions
- **Deprecation process:**
  1. Announce deprecation 6 months in advance via email + API response headers
  2. Add `Sunset` HTTP header with deprecation date
  3. Provide migration guide documentation
  4. 3-month warning period with increased logging
  5. Final sunset with 410 Gone response
- **Breaking change policy:** Major version bump required for any breaking changes
- **B2B SLA:** Enterprise tier guaranteed 18-month backward compatibility

---

## 8. Legal & Compliance Requirements

### 8.1 Content Liability

#### Risk Mitigation
- **Disclaimer:** "Historical analysis tool — not definitive historical truth"
- **Confidence Scoring:** Uncertainty must be explicitly stated
- **No Definitive Claims:** Language must be descriptive, not normative

#### High-Risk Claim Protocol
- Confidence cap at 60% for sensitive claims without primary evidence
- Additional warning labels for claims involving:
  - Collaboration accusations
  - Treason allegations
  - Espionage claims
  - Secret agreements

### 8.2 Copyright Compliance
- Snippet length limitation (fair use compliance)
- Bibliographic reference requirements
- Source attribution enforcement
- No full-text reproduction of copyrighted works

### 8.3 Data Protection (GDPR)
- Explicit consent for data processing
- Right to erasure (case deletion)
- Data portability (export in standard formats)
- Privacy by design (cases private by default)
- Data retention policies (user-configurable, default 2 years)

### 8.4 Terms of Service
- Prohibition on using platform for:
  - Defamation
  - Harassment
  - Misinformation campaigns
  - Academic fraud
- User responsibility for query content
- Platform's right to refuse processing high-risk queries

---

## 9. Academic Validation & Quality Assurance

### 9.1 Advisory Board
- **Composition:**
  - Modern Turkey history expert
  - Diplomatic history specialist
  - European political historian
  - Press/media historian
  - Historical methodology expert
- **Responsibilities:**
  - Source hierarchy validation
  - Scoring system oversight
  - Bias testing protocols
  - Quarterly review meetings

### 9.2 Methodology Whitepaper
- Public documentation of:
  - Evidence weighting mathematics
  - Balance protocol specifications
  - Disagreement handling logic
  - Uncertainty budgeting methodology
- Peer review process
- Version control and updates

### 9.3 External Audit Program
- **Frequency:** Annual
- **Process:**
  - Independent historians review random sample of cases
  - Bias assessment report publication
  - Transparency report publication
  - Recommended improvements implementation

### 9.4 Citation Standards
- Support for Chicago and APA formats
- Persistent Case ID system for referencing
- Academic integrity guidelines
- Plagiarism prevention features

---

## 10. Success Metrics & KPIs

### 10.1 User Engagement Metrics

| Metric | Target (M6) | Target (M12) |
|--------|-------------|--------------|
| Monthly Active Users (MAU) | 5,000 | 25,000 |
| Case Creation Rate | 3/user/month | 5/user/month |
| Average Session Duration | 8 minutes | 12 minutes |
| Return User Rate | 40% | 60% |
| Report Export Rate | 30% | 50% |

### 10.2 Quality Metrics

| Metric | Target |
|--------|--------|
| Source Coverage (MBR compliance) | >80% of cases |
| Citation Traceability | >95% of claims |
| Model Consensus Rate | >70% agreement |
| User Correction Rate | <5% of cases |
| Academic Validation Score | >4.0/5.0 |

### 10.3 Business Metrics

| Metric | Target (M12) |
|--------|--------------|
| Conversion Rate (Free → Paid) | 5% |
| Churn Rate (Monthly) | <5% |
| Net Revenue Retention | >100% |
| Customer Acquisition Cost | <$50 |
| Lifetime Value (LTV) | >$300 |
| LTV:CAC Ratio | >3:1 |

### 10.4 Technical Metrics

| Metric | Target |
|--------|--------|
| System Uptime | 99.9% |
| API Error Rate | <0.1% |
| Average Response Time | <3s |
| Model Timeout Rate | <2% |
| Data Accuracy | >99% |

---

## 11. Release Roadmap

### 11.1 MVP Phase (Weeks 1-4)

#### Week 1: Core Infrastructure
- [ ] API Gateway setup (FastAPI)
- [ ] Proposition Parser Service (NER + temporal inference)
- [ ] Basic Query Expansion (TR/EN)
- [ ] PostgreSQL + Vector DB (pgvector) setup
- [ ] Evidence schema definition
- [ ] Authentication service (JWT)

**Deliverable:** Basic case flow without models

#### Week 2: Retrieval & Evidence
- [ ] Academic collector implementation
- [ ] Basic press collector (TR + EN)
- [ ] Snippet extraction pipeline
- [ ] Reliability scoring v1
- [ ] Evidence Pack builder

**Deliverable:** Evidence panel working

#### Week 3: Multi-Model Integration
- [ ] Model adapters (Gemini, GPT, Claude)
- [ ] JSON strict output validation
- [ ] Error handling and timeouts
- [ ] Partial consensus logic

**Deliverable:** Parallel model outputs functional

#### Week 4: Consensus & UI
- [ ] Claim merging algorithm
- [ ] Weighted scoring implementation (normalized [0,1] range)
- [ ] Disagreement panel UI
- [ ] Timeline v1
- [ ] Confidence label system (Low/Medium/High/Very High)
- [ ] Basic PDF export
- [ ] MBR enforcement with adaptive logic

**Deliverable:** End-to-end working MVP

### 11.2 Post-MVP (Months 2-3)

#### Month 2: Enhancement
- [ ] Ottoman Turkish OCR integration (beta)
- [ ] Advanced NLI contradiction detection
- [ ] Archive connector framework (BOA/BCA, PRO/Kew)
- [ ] Case versioning system
- [ ] User feedback system (correct/incorrect/incomplete marking)
- [ ] A/B testing framework for consensus algorithms

#### Month 3: Polish & Scale
- [ ] Performance optimization (caching, query optimization)
- [ ] Advanced analytics dashboard
- [ ] Mobile responsiveness
- [ ] Onboarding flows
- [ ] Collaborative research features (shared cases, annotations)
- [ ] WCAG 2.1 AA accessibility compliance

### 11.3 v1.0 Launch (Months 4-6)

#### Turkey Launch (Month 4)
- [ ] 5 high-profile case analyses
- [ ] Advisory board announcement
- [ ] Methodology whitepaper release
- [ ] Open beta launch
- [ ] Media outreach campaign

#### Optimization (Months 5-6)
- [ ] User feedback integration
- [ ] B2B pilot programs
- [ ] Academic partnership agreements
- [ ] Monetization optimization
- [ ] Expansion planning

### 11.4 International Expansion (Months 7-18)

#### English Market Entry (Months 7-9)
- [ ] Platform localization (full EN)
- [ ] US/UK academic outreach
- [ ] English content marketing
- [ ] Partnership with research institutes
- [ ] Public sharing links with embeddable widgets

#### European Expansion (Months 10-18)
- [ ] FR, DE, EL full language support
- [ ] European archive integrations (La Courneuve, Gallica)
- [ ] GDPR compliance certification
- [ ] Multi-currency support
- [ ] Offline case access (PWA)

### 11.5 MENA & Eurasia Expansion (Months 18-24)
- [ ] AR, RU full language support
- [ ] Ottoman provincial archive integrations
- [ ] Russian diplomatic archive connectors
- [ ] Right-to-left UI support (Arabic)

---

## 12. Team & Resource Planning

### 12.1 Core Team Requirements

| Role | Count | Phase | Responsibilities |
|------|-------|-------|-----------------|
| Backend Engineer (Senior) | 2 | Month 1+ | FastAPI, model integration, consensus engine |
| Frontend Engineer (Senior) | 1 | Month 1+ | Next.js, timeline/evidence panels, D3.js |
| NLP/ML Engineer | 1 | Month 1+ | NER, query expansion, embedding pipeline, OCR |
| DevOps Engineer | 1 | Month 1+ | K8s, CI/CD, monitoring, infrastructure |
| Product Manager | 1 | Month 1+ | Roadmap, stakeholder management, metrics |
| UX/UI Designer | 1 | Month 2+ | Design system, accessibility, user research |
| QA Engineer | 1 | Month 3+ | Test automation, bias testing, regression |
| Content/Historical Advisor | 1 (part-time) | Month 2+ | Source validation, methodology review |

### 12.2 Hiring Timeline
- **Month 1:** Core team (2 backend + 1 frontend + 1 NLP + 1 DevOps + 1 PM) = 6 FTEs
- **Month 2:** Add UX designer + historical advisor = 7.5 FTEs
- **Month 3:** Add QA engineer = 8.5 FTEs
- **Month 7+:** Scale team for international expansion (add 2-3 engineers)

### 12.3 External Resources
- Advisory Board members (compensated per meeting)
- Translation/localization contractors (Phase 3-4)
- Security audit firm (annual penetration testing)
- Legal counsel (GDPR, content liability)

---

## 13. Collaboration & User Feedback Features

### 13.1 Collaborative Research (FR-COLLAB-001)
- **Research Groups:** Users can create teams and share case files
- **Shared Case Files:** Multiple researchers can annotate the same case
- **Annotation System:** Inline comments on evidence snippets and claims
- **Peer Review Workflow:**
  1. Author creates case analysis
  2. Invites reviewers (1-3)
  3. Reviewers add annotations and approve/reject claims
  4. Author revises based on feedback
  5. Final version published with reviewer credits
- **Access Control:** Owner, Editor, Commenter, Viewer roles
- **Availability:** Pro tier and above

### 13.2 User Feedback Loop (FR-FEEDBACK-001)
- **Claim-Level Feedback:** Users can mark individual claims as:
  - ✅ Accurate
  - ❌ Inaccurate (with correction field)
  - ⚠️ Incomplete (with additional evidence submission)
- **Source Quality Feedback:** Users can flag sources as:
  - Misattributed, outdated, low-quality, or biased
- **Feedback Impact:**
  - Aggregated feedback calibrates reliability scores over time
  - Sources flagged by ≥3 users trigger manual review
  - Claim corrections feed into model prompt improvement
- **Crowdsourced Validation:** Academic-tier users can participate in validation programs, earning credits for reviewing cases

### 13.3 Public Sharing & Embedding
- Shareable case links (read-only, no login required)
- Embeddable evidence panels for blogs/articles (iframe + oEmbed)
- Citation-ready permalinks with persistent Case IDs
- Social media preview cards (Open Graph + Twitter Cards)

---

## 14. Experimentation & Quality Framework

### 14.1 A/B Testing Framework
- **Consensus Algorithm Testing:** Compare alternative scoring formulas on identical case inputs
- **Prompt Optimization:** Test different prompt formats across models to measure output quality
- **UI Experiments:** Feature flags for new panel layouts, visualization types
- **Methodology:** Minimum 100 cases per variant, statistical significance p < 0.05

### 14.2 Evidence Weighting Optimization
- Data-driven coefficient tuning for Reliability Score formula
- Automated monitoring of user correction rates per source type
- Quarterly re-calibration based on aggregated feedback data

### 14.3 Model Performance Benchmarking
- Monthly evaluation of each model's accuracy, latency, and cost
- Model replacement readiness: adapter pattern allows hot-swapping models
- Evaluation dataset: 50 curated historical cases with expert-validated ground truth

---

## 15. Risk Analysis & Mitigation

### 15.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model API failures | Medium | High | Timeout fallbacks, partial consensus, caching |
| Retrieval rate limiting | High | Medium | Politeness protocols, caching, queue management |
| Vector DB performance | Low | High | Proper indexing, scaling, query optimization |
| Data quality issues | Medium | High | Reliability scoring, OCR confidence, human review |

### 15.2 Legal Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Defamation claims | Medium | High | Confidence caps, disclaimers, high-risk detection |
| Copyright infringement | Medium | Medium | Snippet limits, attribution, fair use compliance |
| GDPR violations | Low | High | Privacy by design, legal review, compliance audits |
| Academic fraud | Low | High | Terms of service, usage monitoring, disclaimers |

### 15.3 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low adoption | Medium | High | Free tier, viral features, content marketing |
| Academic credibility | Medium | High | Advisory board, whitepaper, audit program |
| Competition | Medium | Medium | Differentiation, speed to market, partnerships |
| Monetization failure | Low | High | Multiple revenue streams, B2B focus, value demonstration |

### 15.4 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scaling issues | Medium | Medium | Cloud infrastructure, auto-scaling, monitoring |
| Data loss | Low | Critical | Automated backups, disaster recovery, redundancy |
| Security breaches | Low | Critical | Security audits, penetration testing, encryption |
| Team capacity | Medium | Medium | Phased approach, contractor support, prioritization |

---

## 16. Appendices

### Appendix A: Glossary

- **Evidence Pack:** Structured collection of processed sources with reliability scores
- **MBR (Minimum Balance Requirements):** Mandatory source diversity criteria, with adaptive thresholds based on topic scope
- **Steelman:** Presenting the strongest version of a counter-argument
- **Consensus Engine:** Algorithm for merging multi-model outputs into normalized weighted scores
- **Claim:** A specific assertion derived from evidence, scored on [0.0, 1.0]
- **Primary Source:** Contemporary documents, archives, official records
- **Secondary Source:** Academic analysis and interpretation
- **Discourse Evidence:** Press, propaganda, public statements
- **Event Evidence:** Official documents, treaties, verified records
- **Ottoman Turkish OCR:** Specialized optical character recognition for Arabic-script Ottoman Turkish documents
- **Adaptive MBR:** Dynamic adjustment of balance requirements based on topic scope and available sources
- **Graceful Degradation:** System's ability to provide partial results when not all models or sources are available
- **Case File:** Immutable, versioned record of a complete analysis including inputs, evidence, model outputs, and consensus

### Appendix B: Model Output Schema

```json
{
  "definitions_review": ["..."],
  "claims": [{
    "claim_id": "uuid",
    "normalized_text": "string",
    "category": "diplomatic|economic|military|intelligence|propaganda",
    "stance": "support|oppose|neutral",
    "evidence_refs": [{"evidence_id": "uuid", "snippet_id": "uuid"}],
    "evidence_strength_score": 0.0
  }],
  "strongest_evidence": ["..."],
  "strongest_counter_evidence": ["..."],
  "uncertainties": ["..."],
  "bias_risk_notes": ["..."],
  "verdict": {
    "short_statement": "string",
    "confidence_score": 0
  }
}
```

### Appendix C: Technology Stack

**Backend:**
- Python 3.11+ with FastAPI
- PostgreSQL 15+
- Redis 7+
- Pinecone / Weaviate / pgvector
- Celery with RabbitMQ

**Frontend:**
- Next.js 14+
- TypeScript
- Tailwind CSS
- React Query
- D3.js / Chart.js for visualizations

**Infrastructure:**
- Kubernetes (EKS/GKE)
- Docker
- Terraform
- Prometheus + Grafana
- ELK Stack for logging

**AI/ML:**
- Gemini 3.1 Pro Preview API
- GPT-5.2 xhigh API
- Claude Opus 4.6 API
- Sentence Transformers for embeddings
- SpaCy/Transformers for NER
- Tesseract / Azure Document Intelligence for OCR
- Ottoman Turkish OCR specialized model

### Appendix D: Regulatory Compliance Checklist

- [ ] GDPR compliance assessment
- [ ] Terms of Service draft
- [ ] Privacy Policy draft
- [ ] Cookie consent implementation
- [ ] Data processing agreements with providers
- [ ] Copyright policy documentation
- [ ] Content moderation guidelines
- [ ] Incident response plan
- [ ] Security audit completion
- [ ] Accessibility (WCAG 2.1 AA) compliance

### Appendix E: Competitive Analysis

| Feature | PolyHistory | Perplexity | ChatGPT | Traditional Search |
|---------|-------------|------------|---------|-------------------|
| Evidence hierarchy | ✓ | Partial | ✗ | ✗ |
| Multi-model consensus | ✓ | ✗ | ✗ | ✗ |
| Source diversity enforcement | ✓ | ✗ | ✗ | ✗ |
| Cross-national comparison | ✓ | Partial | Partial | Manual |
| Timeline visualization | ✓ | ✗ | ✗ | ✗ |
| Academic citation export | ✓ | Partial | ✗ | Manual |
| Auditability | ✓ | ✗ | ✗ | ✗ |
| Historical focus | ✓ | General | General | General |
| Collaborative research | ✓ | ✗ | ✗ | ✗ |
| Ottoman Turkish OCR | ✓ | ✗ | ✗ | ✗ |
| User feedback loop | ✓ | ✗ | ✗ | ✗ |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-27 | Initial Draft | Document creation |
| 1.0 | 2026-02-27 | Product Team | Final review and approval |
| 2.0 | 2026-03-03 | Product Team | Comprehensive revision: fixed timeline consistency, corrected formulas (Reliability Score, Consensus Engine), added adaptive MBR, redesigned Free Tier, added Ottoman Turkish OCR, cost projections, team planning, collaboration features, experimentation framework, accessibility requirements, API versioning strategy, MENA/Eurasia expansion phase |

**Next Review Date:** 2026-04-03

**Document Owner:** Product Team  
**Stakeholders:** Engineering, Legal, Academic Advisory Board, UX Design

---

*End of Document*
