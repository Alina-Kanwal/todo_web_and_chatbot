/**
 * Empty state component for task list
 * TODO: Implement complete empty state (Task T055)
 */

export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="mb-4 text-4xl">📝</div>
      <h3 className="text-lg font-medium text-gray-900">No tasks yet</h3>
      <p className="mt-1 text-sm text-gray-500">
        Create your first task to get started
      </p>
    </div>
  )
}
