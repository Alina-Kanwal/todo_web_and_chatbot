'use client'

/**
 * Dashboard page - Main task management interface
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { isAuthenticated, getCurrentUserFromToken } from '@/lib/auth'
import { authApi, tasksApi } from '@/lib/api'
import { Task } from '@/types'
import ChatWidget from '@/components/chatbot/ChatWidget'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<{ email: string; user_id: number } | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isCreating, setIsCreating] = useState(false)
  const [newTaskTitle, setNewTaskTitle] = useState('')
  const [newTaskDescription, setNewTaskDescription] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [sortField, setSortField] = useState<string>('created_at')
  const [sortOrder, setSortOrder] = useState<string>('desc')
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')
  const [error, setError] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    // Check authentication on mount
    if (!isAuthenticated()) {
      router.push('/signin')
      return
    }

    const userData = getCurrentUserFromToken()
    setUser(userData)
    loadTasks()
    setIsLoading(false)
  }, [router, statusFilter, sortField, sortOrder])

  const loadTasks = async () => {
    try {
      const loadedTasks = await tasksApi.list(
        statusFilter === 'all' ? undefined : statusFilter,
        sortField,
        sortOrder
      )
      setTasks(loadedTasks)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    }
  }

  const handleSignOut = async () => {
    await authApi.signout()
    router.push('/signin')
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (!newTaskTitle.trim()) {
      setError('Task title is required')
      return
    }

    setIsCreating(true)
    try {
      await tasksApi.create(newTaskTitle.trim(), newTaskDescription.trim() || undefined)
      setNewTaskTitle('')
      setNewTaskDescription('')
      setIsCreating(false)
      setSuccessMessage('Task created successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
      loadTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task')
      setIsCreating(false)
    }
  }

  const handleToggleTask = async (taskId: number) => {
    try {
      await tasksApi.toggle(taskId.toString())
      setSuccessMessage('Task updated!')
      setTimeout(() => setSuccessMessage(''), 3000)
      loadTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
    }
  }

  const handleDeleteTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    
    try {
      await tasksApi.delete(taskId.toString())
      setSuccessMessage('Task deleted successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
      loadTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task')
    }
  }

  const handleStartEdit = (task: Task) => {
    setEditingTaskId(task.id)
    setEditTitle(task.title)
    setEditDescription(task.description || '')
  }

  const handleCancelEdit = () => {
    setEditingTaskId(null)
    setEditTitle('')
    setEditDescription('')
  }

  const handleSaveEdit = async (taskId: number) => {
    if (!editTitle.trim()) {
      setError('Task title is required')
      return
    }

    try {
      await tasksApi.update(taskId.toString(), {
        title: editTitle.trim(),
        description: editDescription.trim() || null,
      })
      setEditingTaskId(null)
      setEditTitle('')
      setEditDescription('')
      setSuccessMessage('Task updated successfully!')
      setTimeout(() => setSuccessMessage(''), 3000)
      loadTasks()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task')
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
          <h1 className="text-xl font-bold text-gray-900">Hackathon Todo</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button
              onClick={handleSignOut}
              className="rounded-md bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8">
        {/* Messages */}
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
        {successMessage && (
          <div className="mb-4 rounded-md bg-green-50 p-4">
            <p className="text-sm text-green-800">{successMessage}</p>
          </div>
        )}

        {/* Create Task Form */}
        <div className="mb-8 rounded-lg bg-white p-6 shadow-md">
          <h2 className="mb-4 text-lg font-semibold text-gray-900">Create New Task</h2>
          <form onSubmit={handleCreateTask} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Title *
              </label>
              <input
                id="title"
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="Enter task title..."
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                placeholder="Enter task description (optional)..."
                rows={3}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={isCreating}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isCreating ? 'Creating...' : 'Create Task'}
            </button>
          </form>
        </div>

        {/* Filters and Sorting */}
        <div className="mb-6 flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="mt-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="all">All</option>
              <option value="pending">Pending</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Sort By</label>
            <select
              value={sortField}
              onChange={(e) => setSortField(e.target.value)}
              className="mt-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="created_at">Date</option>
              <option value="title">Title</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Order</label>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="mt-1 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="desc">Newest First</option>
              <option value="asc">Oldest First</option>
            </select>
          </div>
        </div>

        {/* Task List */}
        <div className="rounded-lg bg-white shadow-md">
          <div className="border-b px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Your Tasks ({tasks.length})
            </h2>
          </div>
          
          {tasks.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <p className="text-gray-500">No tasks yet. Create your first task above!</p>
            </div>
          ) : (
            <ul className="divide-y">
              {tasks.map((task) => (
                <li key={task.id} className="px-6 py-4">
                  {editingTaskId === task.id ? (
                    // Edit Mode
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        rows={2}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleSaveEdit(task.id)}
                          className="rounded-md bg-green-600 px-3 py-1 text-sm font-medium text-white hover:bg-green-700"
                        >
                          Save
                        </button>
                        <button
                          onClick={handleCancelEdit}
                          className="rounded-md bg-gray-200 px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-300"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // View Mode
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() => handleToggleTask(task.id)}
                          className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <div>
                          <h3 className={`font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                            {task.title}
                          </h3>
                          {task.description && (
                            <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                              {task.description}
                            </p>
                          )}
                          <p className="mt-2 text-xs text-gray-400">
                            Created: {new Date(task.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleStartEdit(task)}
                          className="rounded-md bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700 hover:bg-blue-200"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteTask(task.id)}
                          className="rounded-md bg-red-100 px-3 py-1 text-sm font-medium text-red-700 hover:bg-red-200"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>

      {/* Chatbot Widget */}
      <ChatWidget />
    </div>
  )
}
