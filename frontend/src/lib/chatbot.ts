/**
 * Chatbot API client
 */

import { ChatbotResponse } from '@/types/chatbot'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

/**
 * Get stored JWT token
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('jwt_token')
}

/**
 * Send message to chatbot
 */
export async function sendMessage(message: string, conversationId?: string): Promise<ChatbotResponse> {
  const token = getToken()

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      message: 'Failed to send message to chatbot',
    }))
    throw new Error(error.message || 'Failed to send message')
  }

  return response.json()
}
