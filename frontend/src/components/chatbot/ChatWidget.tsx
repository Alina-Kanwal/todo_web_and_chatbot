'use client'

/**
 * ChatWidget component - Floating chat button and panel
 */

import { useState } from 'react'
import ChatPanel from './ChatPanel'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [unreadCount, setUnreadCount] = useState(0)

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 group"
          aria-label="Open chat"
        >
          <div className="relative">
            <svg
              className="w-8 h-8"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            {unreadCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold animate-pulse">
                {unreadCount}
              </span>
            )}
          </div>

          {/* Tooltip */}
          <div className="absolute right-full mr-3 top-1/2 -translate-y-1/2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
            <span>Need help with tasks?</span>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 -mr-1 w-2 h-2 bg-gray-900 rotate-45"></div>
          </div>
        </button>
      )}

      {/* Expanded Chat Panel */}
      {isOpen && (
        <div className="fixed bottom-0 right-6 z-50 w-96 h-[600px] max-h-[calc(100vh-80px)] shadow-2xl">
          <ChatPanel onClose={() => setIsOpen(false)} />
        </div>
      )}
    </>
  )
}
