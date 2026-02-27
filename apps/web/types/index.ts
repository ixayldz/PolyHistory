export interface User {
  id: string
  email: string
  tier: 'free' | 'pro' | 'research' | 'enterprise'
  monthly_analysis_count: number
  monthly_analysis_limit: number
  created_at: string
}

export interface Case {
  id: string
  proposition: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  confidence_score?: number
  created_at: string
}

export interface CaseDetail extends Case {
  normalized_proposition?: Record<string, any>
  time_window?: {
    start?: string
    end?: string
  }
  mbr_compliant: boolean
  mbr_missing_clusters?: Record<string, any>
  verdict?: {
    short_statement: string
  }
  consensus?: ConsensusData
}

export interface EvidenceItem {
  id: string
  title?: string
  author?: string
  publisher?: string
  publication_date?: string
  country?: string
  language?: string
  source_type?: 'primary' | 'secondary' | 'press' | 'memoir' | 'academic'
  stance?: 'pro' | 'contra' | 'neutral'
  reliability_score?: number
  reliability_factors?: Record<string, number>
  url?: string
  biblio_reference?: string
  snippets: Snippet[]
}

export interface Snippet {
  id: string
  text: string
  page_location?: string
  paragraph_number?: number
  quality_score?: number
}

export interface Claim {
  id: string
  claim_id_in_case?: string
  normalized_text: string
  category?: 'diplomatic' | 'economic' | 'military' | 'intelligence' | 'propaganda'
  stance?: 'support' | 'oppose' | 'neutral'
  evidence_strength?: number
  agreement_ratio?: number
  final_score?: number
  confidence_label?: 'low' | 'medium' | 'high'
  is_core_consensus: boolean
  is_disputed: boolean
  dispute_reasons?: string[]
  evidence_refs: EvidenceRef[]
}

export interface EvidenceRef {
  evidence_id: string
  snippet_id: string
}

export interface ConsensusData {
  core_claims: Claim[]
  medium_claims: Claim[]
  disputed_claims: Claim[]
  agreement_matrix: {
    models: string[]
    claims: string[]
    agreement_scores: number[][]
  }
  overall_confidence: number
}

export interface TimelineEvent {
  id: string
  date: string
  track: string
  title: string
  description?: string
  source_id: string
  evidence_type: string
}

export interface CreateCaseInput {
  proposition: string
  time_window?: {
    start?: string
    end?: string
  }
  geography?: string[]
  options?: {
    require_steel_man?: boolean
    source_preference?: 'primary_only' | 'balanced' | 'broad'
    languages?: string[]
  }
}
