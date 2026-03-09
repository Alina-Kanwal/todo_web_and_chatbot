'use client'

/**
 * Debug page to check authentication status
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function DebugPage() {
  const router = useRouter()
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    // Check token
    const storedToken = localStorage.getItem('jwt_token')
    setToken(storedToken)

    if (storedToken) {
      try {
        // Decode JWT to see user info
        const payload = JSON.parse(atob(storedToken.split('.')[1]))
        setUser(payload)
      } catch (e) {
        console.error('Failed to decode token:', e)
      }
    }
  }, [])

  const testSignin = async () => {
    const email = (document.getElementById('test-email') as HTMLInputElement)?.value
    const password = (document.getElementById('test-password') as HTMLInputElement)?.value

    if (!email || !password) {
      alert('Please enter email and password')
      return
    }

    try {
      const response = await fetch('http://localhost:8000/api/auth/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      console.log('Signin response:', data)

      if (response.ok) {
        localStorage.setItem('jwt_token', data.access_token)
        alert('Sign in successful! Token saved.')
        window.location.reload()
      } else {
        alert(`Sign in failed: ${data.message || 'Unknown error'}`)
      }
    } catch (error) {
      console.error('Signin error:', error)
      alert(`Signin error: ${error}`)
    }
  }

  const goToDashboard = () => {
    router.push('/dashboard')
  }

  const clearToken = () => {
    localStorage.removeItem('jwt_token')
    window.location.reload()
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">🔍 Authentication Debug Page</h1>

        {/* Token Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">JWT Token Status</h2>
          {token ? (
            <div className="space-y-2">
              <p className="text-green-600 font-semibold">✅ Token Found!</p>
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm font-mono break-all">
                  <strong>Token:</strong> {token.substring(0, 50)}...
                </p>
              </div>
              {user && (
                <div className="bg-blue-50 p-4 rounded">
                  <p className="text-sm"><strong>User ID:</strong> {user.user_id}</p>
                  <p className="text-sm"><strong>Expires:</strong> {new Date(user.exp * 1000).toLocaleString()}</p>
                </div>
              )}
              <button
                onClick={goToDashboard}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Go to Dashboard →
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-red-600 font-semibold">❌ No Token Found</p>
              <p className="text-sm text-gray-600">You need to sign in first.</p>
            </div>
          )}
          <button
            onClick={clearToken}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Clear Token
          </button>
        </div>

        {/* Test Sign In */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Test Sign In</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                id="test-email"
                type="email"
                defaultValue="test@example.com"
                className="w-full border rounded px-3 py-2"
                placeholder="Enter your email"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <input
                id="test-password"
                type="password"
                defaultValue="password123"
                className="w-full border rounded px-3 py-2"
                placeholder="Enter your password"
              />
            </div>
            <button
              onClick={testSignin}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              Test Sign In
            </button>
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-2">📋 Debug Steps</h2>
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>Check if token is displayed above (✅ or ❌)</li>
            <li>If no token, use "Test Sign In" with your credentials</li>
            <li>After sign in, check console (F12) for errors</li>
            <li>Click "Go to Dashboard" to test redirect</li>
          </ol>
        </div>

        {/* Quick Links */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Links</h2>
          <div className="space-y-2">
            <a href="/signin" className="block text-blue-600 hover:underline">→ Sign In Page</a>
            <a href="/signup" className="block text-blue-600 hover:underline">→ Sign Up Page</a>
            <a href="/dashboard" className="block text-blue-600 hover:underline">→ Dashboard</a>
            <a href="http://localhost:8000/docs" className="block text-blue-600 hover:underline" target="_blank">→ Backend API Docs</a>
          </div>
        </div>
      </div>
    </div>
  )
}
