'use client'

import { useParams } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'

import { api } from '@/lib/api'
import { formatDate } from '@/lib/utils'

export default function CaseDetailPage() {
  const params = useParams<{ id: string }>()
  const caseId = params.id

  const caseQuery = useQuery({
    queryKey: ['case', caseId],
    queryFn: () => api.getCase(caseId),
    enabled: Boolean(caseId),
    refetchInterval: (query) => (query.state.data?.status === 'completed' || query.state.data?.status === 'failed' ? false : 5000),
  })

  const evidenceQuery = useQuery({
    queryKey: ['evidence', caseId],
    queryFn: () => api.getEvidence(caseId),
    enabled: caseQuery.data?.status === 'completed',
  })

  const consensusQuery = useQuery({
    queryKey: ['consensus', caseId],
    queryFn: () => api.getConsensus(caseId),
    enabled: caseQuery.data?.status === 'completed',
  })

  if (caseQuery.isLoading) {
    return <main className="p-8 text-gray-600">Loading case...</main>
  }

  if (caseQuery.error || !caseQuery.data) {
    return <main className="p-8 text-red-600">Case could not be loaded.</main>
  }

  const item = caseQuery.data

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="mx-auto max-w-5xl space-y-6">
        <section className="rounded-lg border bg-white p-6">
          <h1 className="text-2xl font-bold text-gray-900">Case Detail</h1>
          <p className="mt-3 text-gray-800">{item.proposition}</p>
          <div className="mt-4 grid gap-2 text-sm text-gray-600 sm:grid-cols-2">
            <p>Status: <span className="font-medium capitalize">{item.status}</span></p>
            <p>Created: <span className="font-medium">{formatDate(item.created_at)}</span></p>
            <p>
              Confidence:{' '}
              <span className="font-medium">
                {item.confidence_score !== undefined && item.confidence_score !== null
                  ? `${Math.round(item.confidence_score * 100)}%`
                  : 'n/a'}
              </span>
            </p>
            <p>MBR: <span className="font-medium">{item.mbr_compliant ? 'Compliant' : 'Needs attention'}</span></p>
          </div>
          {item.verdict?.short_statement && (
            <div className="mt-4 rounded-md bg-blue-50 p-4 text-sm text-blue-900">
              {item.verdict.short_statement}
            </div>
          )}
        </section>

        <section className="rounded-lg border bg-white p-6">
          <h2 className="mb-4 text-xl font-semibold text-gray-900">Evidence</h2>
          {evidenceQuery.isLoading && <p className="text-gray-600">Loading evidence...</p>}
          {evidenceQuery.error && <p className="text-red-600">Failed to load evidence.</p>}
          {!evidenceQuery.isLoading && !evidenceQuery.error && (
            <div className="space-y-4">
              {evidenceQuery.data?.length ? (
                evidenceQuery.data.map((evidence) => (
                  <article key={evidence.id} className="rounded-md border p-4">
                    <h3 className="font-medium text-gray-900">{evidence.title || 'Untitled'}</h3>
                    <p className="mt-1 text-sm text-gray-600">
                      {evidence.source_type} | {evidence.country} | reliability {evidence.reliability_score ?? 'n/a'}
                    </p>
                    {evidence.snippets?.[0] && (
                      <p className="mt-2 text-sm text-gray-700">{evidence.snippets[0].text}</p>
                    )}
                  </article>
                ))
              ) : (
                <p className="text-gray-500">No evidence available.</p>
              )}
            </div>
          )}
        </section>

        <section className="rounded-lg border bg-white p-6">
          <h2 className="mb-4 text-xl font-semibold text-gray-900">Consensus</h2>
          {consensusQuery.isLoading && item.status === 'completed' && <p className="text-gray-600">Loading consensus...</p>}
          {consensusQuery.error && <p className="text-red-600">Failed to load consensus.</p>}
          {!consensusQuery.isLoading && !consensusQuery.error && consensusQuery.data && (
            <div className="text-sm text-gray-700">
              <p>Overall confidence: {Math.round(consensusQuery.data.overall_confidence * 100)}%</p>
              <p className="mt-2">Core claims: {consensusQuery.data.core_claims.length}</p>
              <p>Disputed claims: {consensusQuery.data.disputed_claims.length}</p>
            </div>
          )}
          {item.status !== 'completed' && (
            <p className="text-gray-600">Consensus becomes available when processing completes.</p>
          )}
        </section>
      </div>
    </main>
  )
}
