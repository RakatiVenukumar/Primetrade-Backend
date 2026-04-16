import { useEffect, useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import type { SessionData } from '../lib/auth'
import { clearSession } from '../lib/auth'

type Task = {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

type TaskListResponse = {
  tasks: Task[]
  total: number
  limit: number
  offset: number
}

type DashboardPageProps = {
  apiBase: string
  session: SessionData
  onLogout: () => void
}

export function DashboardPage({ apiBase, session, onLogout }: DashboardPageProps) {
  const navigate = useNavigate()
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('Loading tasks...')
  const [busyTaskId, setBusyTaskId] = useState<number | null>(null)
  const [isCreating, setIsCreating] = useState(false)

  const authHeaders = useMemo(
    () => ({
      Authorization: `Bearer ${session.token}`,
      'Content-Type': 'application/json',
    }),
    [session.token]
  )

  async function loadTasks() {
    try {
      const response = await fetch(`${apiBase}/tasks?limit=50&offset=0`, {
        headers: {
          Authorization: `Bearer ${session.token}`,
        },
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        setStatus(`Failed to load tasks: ${body?.error?.message ?? 'unknown error'}`)
        return
      }

      const data = (await response.json()) as TaskListResponse
      setTasks(data.tasks)
      setStatus(data.tasks.length ? `Loaded ${data.total} task(s)` : 'No tasks yet')
    } catch {
      setStatus('Network error while loading tasks')
    }
  }

  useEffect(() => {
    void loadTasks()
  }, [])

  async function handleCreateTask(event: FormEvent) {
    event.preventDefault()
    if (!title.trim()) return

    setIsCreating(true)
    setStatus('Creating task...')

    try {
      const response = await fetch(`${apiBase}/tasks`, {
        method: 'POST',
        headers: authHeaders,
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() ? description.trim() : null,
        }),
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        setStatus(`Create failed: ${body?.error?.message ?? 'unknown error'}`)
        return
      }

      setTitle('')
      setDescription('')
      await loadTasks()
    } catch {
      setStatus('Network error while creating task')
    } finally {
      setIsCreating(false)
    }
  }

  async function handleToggleTask(task: Task) {
    setBusyTaskId(task.id)
    setStatus(`Updating task #${task.id}...`)

    try {
      const response = await fetch(`${apiBase}/tasks/${task.id}`, {
        method: 'PUT',
        headers: authHeaders,
        body: JSON.stringify({ completed: !task.completed }),
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        setStatus(`Update failed: ${body?.error?.message ?? 'unknown error'}`)
        return
      }

      await loadTasks()
    } catch {
      setStatus('Network error while updating task')
    } finally {
      setBusyTaskId(null)
    }
  }

  async function handleDeleteTask(taskId: number) {
    setBusyTaskId(taskId)
    setStatus(`Deleting task #${taskId}...`)

    try {
      const response = await fetch(`${apiBase}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${session.token}`,
        },
      })

      if (!response.ok && response.status !== 204) {
        const body = await response.json().catch(() => ({}))
        setStatus(`Delete failed: ${body?.error?.message ?? 'unknown error'}`)
        return
      }

      await loadTasks()
    } catch {
      setStatus('Network error while deleting task')
    } finally {
      setBusyTaskId(null)
    }
  }

  function handleLogout() {
    clearSession()
    onLogout()
    navigate('/login', { replace: true })
  }

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">PrimeTrade Dashboard</p>
        <h1>Welcome, {session.user.email}</h1>
        <p className="subtext">Role: {session.user.role}</p>

        <div className="panel">
          <p><strong>User ID:</strong> {session.user.id}</p>
          <p><strong>API:</strong> {apiBase}</p>
          <p><strong>Access Token:</strong> {session.token.slice(0, 24)}...</p>
          <p><strong>Status:</strong> {status}</p>
        </div>

        <form className="grid task-form" onSubmit={handleCreateTask}>
          <label>
            Task title
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              type="text"
              placeholder="What needs to be done?"
              required
            />
          </label>
          <label>
            Description (optional)
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              type="text"
              placeholder="Additional notes"
            />
          </label>
          <button type="submit" disabled={isCreating}>Add task</button>
        </form>

        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className={task.completed ? 'task done' : 'task'}>
              <div>
                <p className="task-title">{task.title}</p>
                {task.description ? <p className="task-desc">{task.description}</p> : null}
              </div>
              <div className="task-actions">
                <button
                  type="button"
                  onClick={() => handleToggleTask(task)}
                  disabled={busyTaskId === task.id}
                >
                  {task.completed ? 'Mark open' : 'Mark done'}
                </button>
                <button
                  type="button"
                  onClick={() => handleDeleteTask(task.id)}
                  disabled={busyTaskId === task.id}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>

        <div className="actions">
          <button type="button" onClick={handleLogout}>Logout</button>
        </div>
      </section>
    </main>
  )
}
