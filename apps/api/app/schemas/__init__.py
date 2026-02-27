from datetime import datetime, date
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID


# ============== User Schemas ==============

class UserBase(BaseModel):
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    tier: Optional[Literal['free', 'pro', 'research', 'enterprise']] = None


class UserInDB(UserBase):
    id: UUID
    tier: str
    monthly_analysis_count: int
    monthly_analysis_limit: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: UUID
    tier: str
    monthly_analysis_count: int
    monthly_analysis_limit: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============== Auth Schemas ==============

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    type: Optional[str] = None
    exp: Optional[datetime] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ============== Case Schemas ==============

class TimeWindow(BaseModel):
    start: Optional[date] = None
    end: Optional[date] = None


class CaseOptions(BaseModel):
    require_steel_man: bool = True
    source_preference: Literal['primary_only', 'balanced', 'broad'] = 'balanced'
    languages: List[Literal['tr', 'en', 'fr', 'el']] = Field(default=['tr', 'en'])


class CaseCreate(BaseModel):
    proposition: str = Field(..., min_length=10, max_length=1000)
    time_window: Optional[TimeWindow] = None
    geography: Optional[List[str]] = None
    options: CaseOptions = Field(default_factory=CaseOptions)


class CaseUpdate(BaseModel):
    status: Optional[Literal['pending', 'processing', 'completed', 'failed']] = None


class CaseInDB(BaseModel):
    id: UUID
    user_id: UUID
    proposition: str
    normalized_proposition: Optional[Dict[str, Any]] = None
    time_window_start: Optional[date] = None
    time_window_end: Optional[date] = None
    geography: Optional[List[str]] = None
    claim_type: Optional[str] = None
    status: str
    mbr_compliant: bool
    mbr_missing_clusters: Optional[Dict[str, Any]] = None
    verdict_short: Optional[str] = None
    confidence_score: Optional[float] = None
    consensus_output: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    processing_duration_ms: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


class CaseResponse(BaseModel):
    id: UUID
    proposition: str
    status: str
    confidence_score: Optional[float] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class CaseDetailResponse(CaseResponse):
    normalized_proposition: Optional[Dict[str, Any]] = None
    time_window: Optional[TimeWindow] = None
    mbr_compliant: bool
    mbr_missing_clusters: Optional[Dict[str, Any]] = None
    verdict: Optional[Dict[str, Any]] = None
    consensus: Optional[Dict[str, Any]] = None


class CaseListResponse(BaseModel):
    items: List[CaseResponse]
    total: int


# ============== Evidence Schemas ==============

class SnippetResponse(BaseModel):
    id: UUID
    text: str
    page_location: Optional[str] = None
    paragraph_number: Optional[int] = None
    quality_score: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)


class EvidenceItemResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
    country: Optional[str] = None
    language: Optional[str] = None
    source_type: Optional[str] = None
    stance: Optional[str] = None
    reliability_score: Optional[float] = None
    reliability_factors: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    biblio_reference: Optional[str] = None
    snippets: List[SnippetResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class EvidenceFilter(BaseModel):
    source_type: Optional[str] = None
    country: Optional[str] = None
    stance: Optional[str] = None


# ============== Claim Schemas ==============

class EvidenceRef(BaseModel):
    evidence_id: str
    snippet_id: str


class ClaimResponse(BaseModel):
    id: UUID
    claim_id_in_case: Optional[str] = None
    normalized_text: str
    category: Optional[str] = None
    stance: Optional[str] = None
    evidence_strength: Optional[float] = None
    agreement_ratio: Optional[float] = None
    final_score: Optional[float] = None
    confidence_label: Optional[str] = None
    is_core_consensus: bool
    is_disputed: bool
    dispute_reasons: Optional[List[str]] = None
    evidence_refs: List[EvidenceRef] = []
    
    model_config = ConfigDict(from_attributes=True)


# ============== Consensus Schemas ==============

class AgreementMatrix(BaseModel):
    models: List[str]
    claims: List[str]
    agreement_scores: List[List[float]]


class ConsensusAnalysisResponse(BaseModel):
    core_claims: List[ClaimResponse]
    medium_claims: List[ClaimResponse]
    disputed_claims: List[ClaimResponse]
    agreement_matrix: AgreementMatrix
    overall_confidence: float


# ============== Timeline Schemas ==============

class TimelineEvent(BaseModel):
    id: str
    date: date
    track: str
    title: str
    description: Optional[str] = None
    source_id: UUID
    evidence_type: str


# ============== Export Schemas ==============

class ExportRequest(BaseModel):
    format: Literal['markdown', 'pdf', 'json'] = 'markdown'
    citation_style: Literal['apa', 'chicago'] = 'chicago'


class PropositionParsed(BaseModel):
    entities: List[str]
    time_window: TimeWindow
    geography: List[str]
    claim_type: Optional[str] = None
    ambiguity_terms: List[str]
    normalized_definitions: Dict[str, List[str]]
