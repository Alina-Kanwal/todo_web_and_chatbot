'use client'

/**
 * MessageList component - Displays chat messages
 */

import { ChatMessage } from '@/types/chatbot'

interface MessageListProps {
  messages: ChatMessage[]
}

export default function MessageList({ messages }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto space-y-4 p-4">
      {messages.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          <p className="text-lg mb-2">👋 Hi there!</p>
          <p className="text-sm">I'm your Task Assistant. I can help you:</p>
          <ul className="text-sm mt-2 space-y-1">
            <li>✅ Create new tasks</li>
            <li>📋 View your tasks</li>
            <li>✏️ Update existing tasks</li>
            <li>🗑️ Delete tasks</li>
          </ul>
          <p className="text-sm mt-3">Try saying: "Create a task to buy groceries"</p>
        </div>
      ) : (
        messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {message.role === 'assistant' && (
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-semibold">🤖 Task Assistant</span>
                </div>
              )}
              <p className="text-sm whitespace-pre-wrap break-words">
                {message.content}
              </p>
              <p className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-100' : 'text-gray-400'}`}>
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </p>
            </div>
          </div>
        ))
      )}
    </div>
  )
}
