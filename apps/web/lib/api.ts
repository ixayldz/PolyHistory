import axios, { AxiosError, AxiosInstance } from 'axios'
import { 
  User, Case, CaseDetail, EvidenceItem, Claim, 
  ConsensusData, TimelineEvent, CreateCaseInput 
} from '@/types'

const rawApiBase = process.env.NEXT_PUBLIC_API_URL?.trim()
const API_BASE_URL = rawApiBase
  ? (rawApiBase.endsWith('/api/v1') ? rawApiBase : `${rawApiBase.replace(/\/$/, '')}/api/v1`)
  : '/api/v1'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor to add auth token
    this.client.interceptors.request.use((config) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401 && typeof window !== 'undefined') {
          localStorage.removeItem('access_token')
          window.location.href = '/auth/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth
  async register(email: string, password: string): Promise<User> {
    const response = await this.client.post('/auth/register', { email, password })
    return response.data
  }

  async login(email: string, password: string): Promise<{ access_token: string; refresh_token: string }> {
    const response = await this.client.post('/auth/login', { email, password })
    return response.data
  }

  async refresh(refreshToken: string): Promise<{ access_token: string; refresh_token: string }> {
    const response = await this.client.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  // Cases
  async createCase(data: CreateCaseInput): Promise<Case> {
    const response = await this.client.post('/cases', data)
    return response.data
  }

  async listCases(params?: { status?: string; limit?: number; offset?: number }): Promise<{ items: Case[]; total: number }> {
    const response = await this.client.get('/cases', { params })
    return response.data
  }

  async getCase(id: string): Promise<CaseDetail> {
    const response = await this.client.get(`/cases/${id}`)
    return response.data
  }

  async deleteCase(id: string): Promise<void> {
    await this.client.delete(`/cases/${id}`)
  }

  // Evidence
  async getEvidence(caseId: string, filters?: { source_type?: string; country?: string; stance?: string }): Promise<EvidenceItem[]> {
    const response = await this.client.get(`/cases/${caseId}/evidence`, { params: filters })
    return response.data
  }

  // Timeline
  async getTimeline(caseId: string, granularity?: 'day' | 'week' | 'month' | 'year'): Promise<TimelineEvent[]> {
    const response = await this.client.get(`/cases/${caseId}/timeline`, { params: { granularity } })
    return response.data
  }

  // Consensus
  async getConsensus(caseId: string): Promise<ConsensusData> {
    const response = await this.client.get(`/cases/${caseId}/consensus`)
    return response.data
  }

  // Export
  async exportCase(caseId: string, format: 'markdown' | 'pdf' | 'json' = 'markdown'): Promise<Blob> {
    const response = await this.client.post(
      `/cases/${caseId}/export`,
      { format, citation_style: 'chicago' },
      { responseType: 'blob' }
    )
    return response.data
  }
}

export const api = new ApiClient()
