'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'
import { Search, History, FileText, BarChart3, Settings, LogOut, Plus } from 'lucide-react'
import { api } from '@/lib/api'

export default function DashboardPage() {
  const router = useRouter()
  const [proposition, setProposition] = useState('')

  const createCase = useMutation({
    mutationFn: api.createCase,
    onSuccess: (data) => {
      router.push(`/cases/${data.id}`)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (proposition.trim().length >= 10) {
      createCase.mutate({
        proposition: proposition.trim(),
        options: {
          require_steel_man: true,
          source_preference: 'balanced',
          languages: ['tr', 'en'],
        },
      })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <History className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-bold">PolyHistory</span>
          </div>
          <nav className="flex items-center space-x-6">
            <Link href="/cases" className="text-gray-600 hover:text-gray-900 flex items-center space-x-1">
              <FileText className="h-4 w-4" />
              <span>Cases</span>
            </Link>
            <Link href="/analytics" className="text-gray-600 hover:text-gray-900 flex items-center space-x-1">
              <BarChart3 className="h-4 w-4" />
              <span>Analytics</span>
            </Link>
            <Link href="/settings" className="text-gray-600 hover:text-gray-900 flex items-center space-x-1">
              <Settings className="h-4 w-4" />
              <span>Settings</span>
            </Link>
            <button 
              onClick={() => {
                localStorage.removeItem('access_token')
                router.push('/auth/login')
              }}
              className="text-gray-600 hover:text-gray-900 flex items-center space-x-1"
            >
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Evidence-Based Historical Analysis
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Analyze historical propositions using multiple AI models, diverse sources, 
            and cross-national perspectives. Get transparent, evidence-backed insights.
          </p>
        </div>

        {/* Search Input */}
        <div className="max-w-3xl mx-auto mb-12">
          <form onSubmit={handleSubmit} className="relative">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={proposition}
                onChange={(e) => setProposition(e.target.value)}
                placeholder="Enter a historical proposition (e.g., 'Mustafa Kemal Atatürk İngilizlerle iş yaptı mı?')"
                className="w-full pl-12 pr-32 py-4 text-lg border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
              />
              <button
                type="submit"
                disabled={createCase.isPending || proposition.trim().length < 10}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                {createCase.isPending ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>
            <p className="mt-2 text-sm text-gray-500">
              Proposition should be at least 10 characters long
            </p>
          </form>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <FeatureCard
            icon={<Search className="h-6 w-6 text-blue-600" />}
            title="Multi-Source Research"
            description="Automatically gathers sources from archives, academic papers, and period press across multiple languages."
          />
          <FeatureCard
            icon={<BarChart3 className="h-6 w-6 text-green-600" />}
            title="AI Consensus"
            description="Three independent AI models analyze evidence and reach weighted consensus with full transparency."
          />
          <FeatureCard
            icon={<FileText className="h-6 w-6 text-purple-600" />}
            title="Evidence Hierarchy"
            description="Clear source classification with reliability scoring. Primary sources weighted higher than press."
          />
        </div>

        {/* Recent Cases */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b flex items-center justify-between">
            <h2 className="text-lg font-semibold">Recent Analyses</h2>
            <Link 
              href="/cases" 
              className="text-sm text-blue-600 hover:text-blue-700 flex items-center space-x-1"
            >
              <span>View All</span>
              <Plus className="h-4 w-4" />
            </Link>
          </div>
          <div className="p-6 text-center text-gray-500">
            <p>No recent analyses. Start by entering a proposition above.</p>
          </div>
        </div>
      </main>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow border hover:shadow-md transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}
