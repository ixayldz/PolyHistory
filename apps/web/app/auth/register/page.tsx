'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useMutation } from '@tanstack/react-query'

import { api } from '@/lib/api'

export default function RegisterPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const register = useMutation({
    mutationFn: () => api.register(email, password),
    onSuccess: async () => {
      const tokens = await api.login(email, password)
      localStorage.setItem('access_token', tokens.access_token)
      localStorage.setItem('refresh_token', tokens.refresh_token)
      router.push('/')
    },
    onError: (err: any) => {
      setError(err?.response?.data?.error || 'Registration failed')
    },
  })

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-16">
      <div className="mx-auto max-w-md rounded-lg border bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-semibold text-gray-900">Create account</h1>
        <p className="mt-2 text-sm text-gray-600">
          Already registered? <Link href="/auth/login" className="text-blue-700 hover:underline">Sign in</Link>
        </p>

        {error && <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

        <form
          className="mt-6 space-y-4"
          onSubmit={(event) => {
            event.preventDefault()
            setError('')
            register.mutate()
          }}
        >
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full rounded-md border px-3 py-2"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full rounded-md border px-3 py-2"
            />
          </div>
          <button
            type="submit"
            disabled={register.isPending}
            className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {register.isPending ? 'Creating...' : 'Create account'}
          </button>
        </form>
      </div>
    </main>
  )
}
