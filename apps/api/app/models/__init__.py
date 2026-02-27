import uuid
from datetime import datetime
from typing import List, Optional
from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column, String, DateTime, Integer, Boolean, Text, 
    ForeignKey, Table, Float, Date, ARRAY, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


# Junction table for claim-evidence relationship
claim_evidence_table = Table(
    'claim_evidence',
    Base.metadata,
    Column('claim_id', UUID(as_uuid=True), ForeignKey('claims.id', ondelete='CASCADE'), primary_key=True),
    Column('snippet_id', UUID(as_uuid=True), ForeignKey('snippets.id', ondelete='CASCADE'), primary_key=True),
    Column('evidence_weight', Float, default=1.0),
    Column('is_counter_evidence', Boolean, default=False)
)


class User(Base):
    """User model for authentication and billing."""
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)
    
    # Subscription tier
    tier = Column(String(50), default='free', nullable=False)  # free, pro, research, enterprise
    monthly_analysis_count = Column(Integer, default=0, nullable=False)
    monthly_analysis_limit = Column(Integer, default=5, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    cases = relationship("Case", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.tier})>"


class Case(Base):
    """Case model for historical analysis requests."""
    __tablename__ = 'cases'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Input data
    proposition = Column(Text, nullable=False)
    normalized_proposition = Column(JSON, nullable=True)
    time_window_start = Column(Date, nullable=True)
    time_window_end = Column(Date, nullable=True)
    geography = Column(ARRAY(String(100)), nullable=True)
    claim_type = Column(String(50), nullable=True)  # diplomatic, economic, military, intelligence, propaganda
    
    # Processing status
    status = Column(String(50), default='pending', nullable=False, index=True)  # pending, processing, completed, failed
    
    # Minimum Balance Requirements (MBR)
    mbr_compliant = Column(Boolean, default=False, nullable=False)
    mbr_missing_clusters = Column(JSON, nullable=True)
    
    # Results
    verdict_short = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    consensus_output = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    processing_duration_ms = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="cases")
    evidence_items = relationship("EvidenceItem", back_populates="case", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="case", cascade="all, delete-orphan")
    model_outputs = relationship("ModelOutput", back_populates="case", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="case")
    
    def __repr__(self):
        return f"<Case(id={self.id}, status={self.status}, user_id={self.user_id})>"


class EvidenceItem(Base):
    """Evidence source item."""
    __tablename__ = 'evidence_items'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Source metadata
    title = Column(String(500), nullable=True)
    author = Column(String(255), nullable=True)
    publisher = Column(String(255), nullable=True)
    publication_date = Column(Date, nullable=True)
    country = Column(String(100), nullable=True, index=True)
    language = Column(String(10), nullable=True, index=True)
    
    # Classification
    source_type = Column(String(50), nullable=True, index=True)  # primary, secondary, press, memoir, academic
    stance = Column(String(20), nullable=True, index=True)  # pro, contra, neutral
    
    # Scoring
    reliability_score = Column(Float, nullable=True)
    reliability_factors = Column(JSON, nullable=True)
    
    # Reference
    url = Column(Text, nullable=True)
    archive_id = Column(String(255), nullable=True)
    biblio_reference = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    case = relationship("Case", back_populates="evidence_items")
    snippets = relationship("Snippet", back_populates="evidence_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<EvidenceItem(id={self.id}, type={self.source_type}, country={self.country})>"


class Snippet(Base):
    """Text snippet from evidence source."""
    __tablename__ = 'snippets'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evidence_id = Column(UUID(as_uuid=True), ForeignKey('evidence_items.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Content
    text = Column(Text, nullable=False)
    page_location = Column(String(100), nullable=True)
    paragraph_number = Column(Integer, nullable=True)
    quality_score = Column(Float, nullable=True)
    
    # Vector embedding for semantic search
    embedding = Column(Vector(384), nullable=True)  # pgvector
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    evidence_item = relationship("EvidenceItem", back_populates="snippets")
    
    def __repr__(self):
        return f"<Snippet(id={self.id}, evidence_id={self.evidence_id})>"


class Claim(Base):
    """Normalized claim from model analysis."""
    __tablename__ = 'claims'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False, index=True)
    claim_id_in_case = Column(String(100), nullable=True)
    
    # Content
    normalized_text = Column(Text, nullable=False)
    category = Column(String(50), nullable=True)  # diplomatic, economic, military, intelligence, propaganda
    stance = Column(String(20), nullable=True, index=True)  # support, oppose, neutral
    
    # Consensus scoring
    evidence_strength = Column(Float, nullable=True)
    agreement_ratio = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True, index=True)
    confidence_label = Column(String(20), nullable=True, index=True)  # low, medium, high
    
    # Status
    is_core_consensus = Column(Boolean, default=False, nullable=False, index=True)
    is_disputed = Column(Boolean, default=False, nullable=False, index=True)
    dispute_reasons = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    case = relationship("Case", back_populates="claims")
    snippets = relationship("Snippet", secondary=claim_evidence_table, backref="claims")
    
    def __repr__(self):
        return f"<Claim(id={self.id}, confidence={self.confidence_label}, disputed={self.is_disputed})>"


class ModelOutput(Base):
    """Raw output from AI model judges."""
    __tablename__ = 'model_outputs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id', ondelete='CASCADE'), nullable=False, index=True)
    
    model_name = Column(String(50), nullable=False)  # gemini, gpt, claude
    output_json = Column(JSON, nullable=False)
    latency_ms = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)  # success, timeout, error
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    case = relationship("Case", back_populates="model_outputs")
    
    def __repr__(self):
        return f"<ModelOutput(id={self.id}, model={self.model_name}, status={self.status})>"


class AuditLog(Base):
    """Audit trail for all actions."""
    __tablename__ = 'audit_logs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id = Column(UUID(as_uuid=True), ForeignKey('cases.id', ondelete='SET NULL'), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    
    action = Column(String(100), nullable=False, index=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    case = relationship("Case", back_populates="audit_logs")
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action})>"
