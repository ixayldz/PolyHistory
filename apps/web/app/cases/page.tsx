'use client'

import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'

import { api } from '@/lib/api'
import { formatDate } from '@/lib/utils'

export default function CasesPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['cases'],
    queryFn: () => api.listCases({ limit: 50, offset: 0 }),
  })

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8">
      <div className="mx-auto max-w-5xl">
        <h1 className="mb-6 text-2xl font-bold text-gray-900">Cases</h1>

        {isLoading && <p className="text-gray-600">Loading cases...</p>}
        {error && <p className="text-red-600">Failed to load cases.</p>}

        {!isLoading && !error && (
          <div className="overflow-hidden rounded-lg border bg-white">
            <table className="w-full text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-3 text-left">Proposition</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Confidence</th>
                  <th className="px-4 py-3 text-left">Created</th>
                </tr>
              </thead>
              <tbody>
                {data?.items.length ? (
                  data.items.map((item) => (
                    <tr key={item.id} className="border-t">
                      <td className="px-4 py-3">
                        <Link href={`/cases/${item.id}`} className="text-blue-700 hover:underline">
                          {item.proposition}
                        </Link>
                      </td>
                      <td className="px-4 py-3 capitalize">{item.status}</td>
                      <td className="px-4 py-3">
                        {item.confidence_score !== undefined && item.confidence_score !== null
                          ? `${Math.round(item.confidence_score * 100)}%`
                          : 'n/a'}
                      </td>
                      <td className="px-4 py-3">{formatDate(item.created_at)}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="px-4 py-8 text-center text-gray-500">
                      No cases found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </main>
  )
}
