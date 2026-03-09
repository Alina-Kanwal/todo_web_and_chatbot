/**
 * API client for backend communication
 * TODO: Implement complete API methods (Task T049)
 */

import { Task, AuthTokens, ApiError } from '@/types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

/**
 * Get stored JWT token
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('jwt_token')
}

/**
 * Store JWT token
 */
function setToken(token: string): void {
  if (typeof window === 'undefined') return
  localStorage.setItem('jwt_token', token)
}

/**
 * Remove JWT token
 */
function removeToken(): void {
  if (typeof window === 'undefined') return
  localStorage.removeItem('jwt_token')
}

/**
 * Make authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken()

  // Build headers object with proper typing
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }

  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  // Merge any additional headers from options
  if (options.headers) {
    const additionalHeaders = options.headers as Record<string, string>
    Object.assign(headers, additionalHeaders)
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      status_code: response.status,
      error_type: 'UnknownError',
      message: 'An unexpected error occurred',
    }))
    throw new Error(error.message)
  }

  return response.json()
}

// Auth API methods
export const authApi = {
  signup: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        status_code: response.status,
        error_type: 'UnknownError',
        message: 'An unexpected error occurred',
      }))
      throw new Error(error.message)
    }

    const data = await response.json()
    setToken(data.access_token)
    return data
  },

  signin: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        status_code: response.status,
        error_type: 'UnknownError',
        message: 'An unexpected error occurred',
      }))
      throw new Error(error.message)
    }

    const data = await response.json()
    setToken(data.access_token)
    return data
  },

  signout: async () => {
    try {
      await apiRequest('/api/auth/signout', { method: 'POST' })
    } catch (error) {
      // Ignore errors on signout
    }
    removeToken()
  },

  getCurrentUser: async () => {
    return apiRequest('/api/auth/me')
  },
}

// Task API methods
export const tasksApi = {
  list: async (status?: string, sort?: string, order?: string): Promise<Task[]> => {
    const params = new URLSearchParams()
    if (status) params.append('status', status)
    if (sort) params.append('sort', sort)
    if (order) params.append('order', order)

    const response = await apiRequest<{ tasks: Task[] }>(`/api/tasks?${params.toString()}`)
    return response.tasks
  },

  create: async (title: string, description?: string): Promise<Task> => {
    return apiRequest('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    })
  },

  get: async (id: string): Promise<Task> => {
    return apiRequest(`/api/tasks/${id}`)
  },

  update: async (id: string, updates: Partial<Task>): Promise<Task> => {
    return apiRequest(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    })
  },

  patch: async (id: string, updates: Partial<Task>): Promise<Task> => {
    return apiRequest(`/api/tasks/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    })
  },

  delete: async (id: string): Promise<void> => {
    await apiRequest(`/api/tasks/${id}`, {
      method: 'DELETE',
    })
  },

  toggle: async (id: string): Promise<Task> => {
    return apiRequest(`/api/tasks/${id}/toggle`, {
      method: 'POST',
    })
  },
}

// Auth hook for React components
export function useAuth() {
  return {
    isAuthenticated: isAuthenticated(),
    user: getCurrentUserFromToken(),
    isLoading: false,
  }
}

export { getToken, setToken, removeToken }
