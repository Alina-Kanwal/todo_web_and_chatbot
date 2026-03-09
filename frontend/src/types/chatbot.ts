/**
 * Chatbot type definitions
 */

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
}

export interface ChatbotResponse {
  response: string
  actions_performed?: Array<{
    type: string
    task_id?: number
    details: any
  }>
  conversation_id?: string
}

export interface ChatbotState {
  isOpen: boolean
  messages: ChatMessage[]
  isLoading: boolean
  conversationId: string | null
}
