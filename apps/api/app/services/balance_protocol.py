"""
Balance Protocol Service
Enforces Minimum Balance Requirements (MBR) for source diversity.
"""

from typing import List, Dict, Any, Set
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app import models
from app.core.config import get_settings

settings = get_settings()


@dataclass
class MBRStatus:
    """Minimum Balance Requirements status."""
    compliant: bool
    missing_clusters: Dict[str, Any]
    details: Dict[str, Any]
    topic_scope: str = "international"
    user_override: bool = False


class BalanceProtocol:
    """
    Enforce Minimum Balance Requirements (MBR) for historical analysis.
    
    Adaptive MBR (PRD v2.0):
    - International topics: Foreign_countries >= 2
    - Domestic-only topics: Foreign_countries >= 1 (preference for 2)
    - Common: TR_sources >= 2, Pro >= 1, Contra >= 1
    """
    
    def __init__(self):
        pass
    
    def check_minimum_balance(
        self,
        case_id: str,
        evidence_items: List[models.EvidenceItem],
        topic_scope: str = "international"
    ) -> MBRStatus:
        """
        Check if evidence pack meets MBR criteria.
        
        Args:
            case_id: UUID of the case
            evidence_items: List of evidence items
            
        Returns:
            MBRStatus with compliance info
        """
        missing_clusters = {}
        details = {
            "tr_count": 0,
            "foreign_countries": set(),
            "pro_count": 0,
            "contra_count": 0,
            "tr_primary_academic": 0,
            "tr_press": 0,
            "foreign_press": 0,
            "foreign_official_academic": 0,
        }
        
        # Analyze evidence
        for item in evidence_items:
            country = item.country
            stance = item.stance
            source_type = item.source_type
            
            # TR sources
            if country and country.lower() in ["tr", "turkey", "türkiye", "turkiye"]:
                details["tr_count"] += 1
                
                if source_type in ["primary", "academic"]:
                    details["tr_primary_academic"] += 1
                elif source_type == "press":
                    details["tr_press"] += 1
            
            # Foreign sources
            elif country:
                details["foreign_countries"].add(country.lower())
                
                if source_type == "press":
                    details["foreign_press"] += 1
                elif source_type in ["primary", "academic", "official"]:
                    details["foreign_official_academic"] += 1
            
            # Stance
            if stance == "pro":
                details["pro_count"] += 1
            elif stance == "contra":
                details["contra_count"] += 1
        
        # Check requirements
        compliant = True
        
        # Check TR sources >= 2
        if details["tr_count"] < 2:
            compliant = False
            missing_clusters["tr_sources"] = {
                "required": 2,
                "found": details["tr_count"],
                "message": "At least 2 Turkish sources required"
            }
        
        # Check TR cluster minimums
        if details["tr_primary_academic"] < 1:
            compliant = False
            missing_clusters["tr_primary_academic"] = {
                "required": 1,
                "found": details["tr_primary_academic"],
                "message": "At least 1 Turkish primary/academic source required"
            }
        
        if details["tr_press"] < 1:
            compliant = False
            missing_clusters["tr_press"] = {
                "required": 1,
                "found": details["tr_press"],
                "message": "At least 1 Turkish press source required"
            }
        
        # Check foreign countries — adaptive based on topic_scope
        min_foreign = 2 if topic_scope == "international" else 1
        if len(details["foreign_countries"]) < min_foreign:
            compliant = False
            suggested = ["UK", "France", "Germany", "Russia"]
            existing = set(details["foreign_countries"])
            suggestions = [c for c in suggested if c.lower() not in existing][:2]
            missing_clusters["foreign_countries"] = {
                "required": min_foreign,
                "found": len(details["foreign_countries"]),
                "countries": list(details["foreign_countries"]),
                "message": f"Sources from at least {min_foreign} foreign countries required",
                "suggested_search_terms": suggestions,
            }
        
        # Check foreign cluster minimums
        if details["foreign_press"] < 1:
            compliant = False
            missing_clusters["foreign_press"] = {
                "required": 1,
                "found": details["foreign_press"],
                "message": "At least 1 foreign press source required"
            }
        
        if details["foreign_official_academic"] < 1:
            compliant = False
            missing_clusters["foreign_official_academic"] = {
                "required": 1,
                "found": details["foreign_official_academic"],
                "message": "At least 1 foreign official/academic source required"
            }
        
        # Check pro stance >= 1
        if details["pro_count"] < 1:
            compliant = False
            missing_clusters["pro_stance"] = {
                "required": 1,
                "found": details["pro_count"],
                "message": "At least 1 pro-stance source required"
            }
        
        # Check contra stance >= 1
        if details["contra_count"] < 1:
            compliant = False
            missing_clusters["contra_stance"] = {
                "required": 1,
                "found": details["contra_count"],
                "message": "At least 1 contra-stance source required"
            }
        
        # Convert set to list for JSON serialization
        details["foreign_countries"] = list(details["foreign_countries"])
        
        return MBRStatus(
            compliant=compliant,
            missing_clusters=missing_clusters,
            details=details,
            topic_scope=topic_scope,
        )
    
    def apply_penalty(self, confidence_score: float) -> float:
        """Apply MBR penalty to confidence score."""
        penalty = settings.MBR_PENALTY_PERCENTAGE / 100
        return confidence_score * (1 - penalty)
    
    def check_high_risk_claim(
        self,
        claim_text: str,
        has_primary_evidence: bool
    ) -> Dict[str, Any]:
        """
        Check for high-risk claims that require special handling.
        
        High-risk keywords: işbirliği, ihanet, gizli anlaşma, casusluk, entrika
        """
        high_risk_keywords = [
            "işbirliği", "iş birliği", "collaboration",
            "ihanet", "treason", "betrayal",
            "gizli anlaşma", "secret agreement", "secret deal",
            "casusluk", "espionage", "spying",
            "entrika", "intrigue",
        ]
        
        claim_lower = claim_text.lower()
        is_high_risk = any(keyword in claim_lower for keyword in high_risk_keywords)
        
        result = {
            "is_high_risk": is_high_risk,
            "has_primary_evidence": has_primary_evidence,
            "confidence_cap": None,
            "warning": None
        }
        
        if is_high_risk and not has_primary_evidence:
            result["confidence_cap"] = settings.HIGH_RISK_CONFIDENCE_CAP
            result["warning"] = (
                "High-risk claim detected without primary evidence. "
                f"Confidence capped at {settings.HIGH_RISK_CONFIDENCE_CAP * 100}%."
            )
        
        return result
    
    def classify_discourse_vs_event(
        self,
        evidence_items: List[models.EvidenceItem]
    ) -> Dict[str, List[models.EvidenceItem]]:
        """
        Separate discourse evidence from event evidence.
        
        Discourse = press, propaganda, public statements
        Event = official documents, treaties, verified records
        """
        discourse_types = ["press", "propaganda", "statement"]
        event_types = ["primary", "treaty", "official", "archival"]
        
        discourse = []
        event = []
        
        for item in evidence_items:
            if item.source_type in discourse_types:
                discourse.append(item)
            elif item.source_type in event_types:
                event.append(item)
            else:
                # Default to discourse for unclassified
                discourse.append(item)
        
        return {
            "discourse": discourse,
            "event": event
        }
