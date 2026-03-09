/**
 * TypeScript type definitions
 */

export interface User {
  id: number
  email: string
  created_at: string
}

export interface Task {
  id: number
  user_id: number
  title: string
  description?: string | null
  completed: boolean
  created_at: string
  updated_at?: string | null
}

export interface AuthTokens {
  access_token: string
  token_type: string
  expires_in?: number
}

export interface ApiError {
  status_code: number
  error_type: string
  message: string
  details?: Record<string, string>
}
