# Product Requirements Document (PRD)
## PolyHistory: Evidence-First Multi-Perspective Historical Analysis Platform

**Version:** 1.0  
**Date:** February 27, 2026  
**Status:** Draft  
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
4. **Halucination Risks:** AI systems generating claims without verifiable evidence
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
| Launch MVP in Turkey | 1000 active users | Month 4 |
| Establish academic credibility | 5 university partnerships | Month 6 |
| Expand to English-speaking markets | US/UK user base growth | Month 9 |
| Achieve profitability | Positive unit economics | Month 12 |
| Global archive integration | 10 institutional partnerships | Month 18 |

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

#### Phase 1: Turkey (Months 1-6)
- Target: University history departments, journalists, content creators
- Positioning: "Çok Kaynaklı Tarih Analiz Platformu" (Non-political)

#### Phase 2: English Markets (Months 7-12)
- Target: US/UK academic institutions, policy research institutes
- Positioning: "Evidence-first historical analysis engine"

#### Phase 3: European Expansion (Months 13-18)
- Add FR/EL full support
- Target: European diplomatic history researchers

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
- **Supported Languages:** TR, EN, FR, EL (Phase 1); DE, RU, AR (Phase 2)
- **Capabilities:**
  - Period terminology mapping (e.g., "Angora Government" ↔ "Ankara Government")
  - Actor name variants (e.g., "Mustafa Kemal" ↔ "Kemal Pasha")
  - Institution and location mappings
  - Keyword clustering (treaty, correspondence, dispatch, communiqué)

#### 5.2.3 Retrieval Cluster (FR-BE-003)
- **Sub-components:**
  - **Academic Collector:** Article metadata, open-access PDFs, bibliographic records
  - **Archive Collector:** Catalog queries, document reference numbers
  - **Press Collector:** Period newspapers, magazine archives
  - **Treaty/Official Text Collector:** Agreement texts, parliamentary records, diplomatic correspondence indices
- **Requirements:**
  - Rate limiting and politeness protocols
  - Caching layer for frequent queries
  - Source reliability pre-scoring

#### 5.2.4 Text Processing Pipeline (FR-BE-004)
- **Stages:**
  1. Document fetch with retry logic
  2. OCR processing (when needed) with confidence scoring
  3. Language detection
  4. Text normalization and cleaning
  5. Semantic chunking
  6. Embedding generation
  7. Metadata enrichment
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
  ```
  Reliability = (Type_Weight × 0.4) + 
                (Institution_Reputation × 0.25) + 
                (Citation_Density × 0.15) + 
                (Cross_Source_Consistency × 0.15) + 
                (OCR_Confidence × 0.05)
  ```

#### 5.2.6 Multi-Model Judge Layer (FR-BE-006)
- **Models:**
  - Gemini 3.1 Pro Preview (broad context synthesis)
  - GPT-5.2 xhigh (claim decomposition, consistency checking)
  - Claude Opus 4.6 (steel-man argumentation, nuanced interpretation)
- **Requirements:**
  - Async parallel execution
  - Timeout handling with fallback
  - Strict JSON output validation
  - Claim-to-evidence referential integrity
  - Partial consensus support (2/3 models)

#### 5.2.7 Consensus Engine (FR-BE-007)
- **Claim Graph Construction:**
  - Semantic similarity matching (threshold: ≥0.85)
  - Claim merging and normalization
  - Graph node creation per normalized claim
- **Evidence Aggregation:**
  ```
  Evidence_Strength = Σ(Adjusted_Weight for claim)
  Adjusted_Weight = Source_Type_Weight × Reliability_Score
  ```
- **Agreement Score:**
  ```
  Agreement_Ratio = Supporting_Models / Total_Models
  Final_Claim_Score = Agreement_Ratio × Evidence_Strength
  ```
- **Confidence Labels:**
  - Low: 0.00–0.30
  - Medium: 0.31–0.60
  - High: 0.61–1.00

#### 5.2.8 Balance Protocol Enforcement (FR-BE-008)
- **Minimum Balance Requirements (MBR):**
  - TR_sources ≥ 2
  - Foreign_countries ≥ 2
  - Pro_stance_sources ≥ 1
  - Contra_stance_sources ≥ 1
- **Source Cluster Minimums:**
  - Turkey: ≥1 primary/academic + ≥1 press
  - Foreign: ≥1 press + ≥1 official/academic
- **Enforcement Actions (if MBR not met):**
  1. Confidence score penalty: -20%
  2. Verdict annotation: "Balance requirement not fully satisfied"
  3. UI warning with missing cluster listing

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
- Automated backup (daily snapshots, 30-day retention)
- Graceful degradation (partial results if one model fails)
- Circuit breaker pattern for external APIs

### 6.5 Auditability Requirements
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
  - 5 analyses per month
  - Single model only
  - Limited source visibility (top 10)
  - No PDF export
  - Basic timeline only
- **Goal:** User acquisition and viral growth

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
- [ ] Proposition Parser Service
- [ ] Basic Query Expansion (TR/EN)
- [ ] PostgreSQL + Vector DB setup
- [ ] Evidence schema definition

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
- [ ] Weighted scoring implementation
- [ ] Disagreement panel UI
- [ ] Timeline v1
- [ ] Confidence label system
- [ ] Basic PDF export

**Deliverable:** End-to-end working MVP

### 11.2 Post-MVP (Months 2-3)

#### Month 2: Enhancement
- [ ] FR + EL language support
- [ ] Advanced NLI contradiction detection
- [ ] Archive connector framework
- [ ] Case versioning system
- [ ] Public sharing links

#### Month 3: Polish & Scale
- [ ] Performance optimization
- [ ] Advanced analytics dashboard
- [ ] Mobile responsiveness
- [ ] Onboarding flows
- [ ] Feedback loop implementation

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

### 11.4 International Expansion (Months 7-12)

#### English Market Entry (Months 7-9)
- [ ] Platform localization
- [ ] US/UK academic outreach
- [ ] English content marketing
- [ ] Partnership with research institutes

#### European Expansion (Months 10-12)
- [ ] FR/EL full support
- [ ] European archive integrations
- [ ] GDPR compliance certification
- [ ] Multi-currency support

---

## 12. Risk Analysis & Mitigation

### 12.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model API failures | Medium | High | Timeout fallbacks, partial consensus, caching |
| Retrieval rate limiting | High | Medium | Politeness protocols, caching, queue management |
| Vector DB performance | Low | High | Proper indexing, scaling, query optimization |
| Data quality issues | Medium | High | Reliability scoring, OCR confidence, human review |

### 12.2 Legal Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Defamation claims | Medium | High | Confidence caps, disclaimers, high-risk detection |
| Copyright infringement | Medium | Medium | Snippet limits, attribution, fair use compliance |
| GDPR violations | Low | High | Privacy by design, legal review, compliance audits |
| Academic fraud | Low | High | Terms of service, usage monitoring, disclaimers |

### 12.3 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low adoption | Medium | High | Free tier, viral features, content marketing |
| Academic credibility | Medium | High | Advisory board, whitepaper, audit program |
| Competition | Medium | Medium | Differentiation, speed to market, partnerships |
| Monetization failure | Low | High | Multiple revenue streams, B2B focus, value demonstration |

### 12.4 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scaling issues | Medium | Medium | Cloud infrastructure, auto-scaling, monitoring |
| Data loss | Low | Critical | Automated backups, disaster recovery, redundancy |
| Security breaches | Low | Critical | Security audits, penetration testing, encryption |
| Team capacity | Medium | Medium | Phased approach, contractor support, prioritization |

---

## 13. Appendices

### Appendix A: Glossary

- **Evidence Pack:** Structured collection of processed sources with reliability scores
- **MBR (Minimum Balance Requirements):** Mandatory source diversity criteria
- **Steelman:** Presenting the strongest version of a counter-argument
- **Consensus Engine:** Algorithm for merging multi-model outputs into weighted scores
- **Claim:** A specific assertion derived from evidence
- **Primary Source:** Contemporary documents, archives, official records
- **Secondary Source:** Academic analysis and interpretation
- **Discourse Evidence:** Press, propaganda, public statements
- **Event Evidence:** Official documents, treaties, verified records

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

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-02-27 | Initial Draft | Document creation |
| 1.0 | 2026-02-27 | Product Team | Final review and approval |

**Next Review Date:** 2026-03-27

**Document Owner:** Product Team  
**Stakeholders:** Engineering, Legal, Academic Advisory Board

---

*End of Document*
