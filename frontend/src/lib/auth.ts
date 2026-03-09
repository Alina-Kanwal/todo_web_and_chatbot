/**
 * Authentication utilities
 */

import { getToken, setToken, removeToken } from './api'
import { authApi } from './api'

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  const token = getToken()
  if (!token) return false

  // Decode JWT to check expiry
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    if (payload.exp && payload.exp * 1000 < Date.now()) {
      return false
    }
    return true
  } catch {
    return false
  }
}

/**
 * Get current user from token
 */
export function getCurrentUserFromToken(): { email: string; user_id: number } | null {
  const token = getToken()
  if (!token) return null

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      email: payload.email,
      user_id: payload.user_id,
    }
  } catch {
    return null
  }
}

/**
 * Get current user info from API
 */
export async function getCurrentUser(): Promise<{ email: string; user_id: number } | null> {
  if (!isAuthenticated()) return null

  try {
    const user = await authApi.getCurrentUser()
    return user
  } catch {
    return null
  }
}
