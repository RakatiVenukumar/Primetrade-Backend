import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import type { SessionData } from '../lib/auth'
import { clearSession } from '../lib/auth'
import { ApiError, apiRequest, apiRequestNoContent } from '../lib/api'

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

type StatusTone = 'info' | 'success' | 'error'

export function DashboardPage({ apiBase, session, onLogout }: DashboardPageProps) {
  const navigate = useNavigate()
  const [tasks, setTasks] = useState<Task[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('Loading tasks...')
  const [statusTone, setStatusTone] = useState<StatusTone>('info')
  const [busyTaskId, setBusyTaskId] = useState<number | null>(null)
  const [isCreating, setIsCreating] = useState(false)

  function handleSessionExpired() {
    clearSession()
    onLogout()
    navigate('/login', { replace: true })
  }

  async function loadTasks() {
    try {
      const data = await apiRequest<TaskListResponse>(
        `${apiBase}/tasks?limit=50&offset=0`,
        {},
        session.token
      )
      setTasks(data.tasks)
      setStatus(data.tasks.length ? `Loaded ${data.total} task(s)` : 'No tasks yet')
      setStatusTone('success')
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        setStatus('Session expired. Please login again.')
        setStatusTone('error')
        handleSessionExpired()
        return
      }

      if (error instanceof ApiError) {
        setStatus(`Failed to load tasks: ${error.message}`)
      } else {
        setStatus('Network error while loading tasks')
      }
      setStatusTone('error')
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
    setStatusTone('info')

    try {
      await apiRequest<Task>(`${apiBase}/tasks`, {
        method: 'POST',
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() ? description.trim() : null,
        }),
      }, session.token)

      setTitle('')
      setDescription('')
      await loadTasks()
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        setStatus('Session expired. Please login again.')
        setStatusTone('error')
        handleSessionExpired()
        return
      }

      if (error instanceof ApiError) {
        setStatus(`Create failed: ${error.message}`)
      } else {
        setStatus('Network error while creating task')
      }
      setStatusTone('error')
    } finally {
      setIsCreating(false)
    }
  }

  async function handleToggleTask(task: Task) {
    setBusyTaskId(task.id)
    setStatus(`Updating task #${task.id}...`)
    setStatusTone('info')

    try {
      await apiRequest<Task>(`${apiBase}/tasks/${task.id}`, {
        method: 'PUT',
        body: JSON.stringify({ completed: !task.completed }),
      }, session.token)

      await loadTasks()
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        setStatus('Session expired. Please login again.')
        setStatusTone('error')
        handleSessionExpired()
        return
      }

      if (error instanceof ApiError) {
        setStatus(`Update failed: ${error.message}`)
      } else {
        setStatus('Network error while updating task')
      }
      setStatusTone('error')
    } finally {
      setBusyTaskId(null)
    }
  }

  async function handleDeleteTask(taskId: number) {
    setBusyTaskId(taskId)
    setStatus(`Deleting task #${taskId}...`)
    setStatusTone('info')

    try {
      await apiRequestNoContent(`${apiBase}/tasks/${taskId}`, {
        method: 'DELETE',
      }, session.token)

      await loadTasks()
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        setStatus('Session expired. Please login again.')
        setStatusTone('error')
        handleSessionExpired()
        return
      }

      if (error instanceof ApiError) {
        setStatus(`Delete failed: ${error.message}`)
      } else {
        setStatus('Network error while deleting task')
      }
      setStatusTone('error')
    } finally {
      setBusyTaskId(null)
    }
  }

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">PrimeTrade Dashboard</p>
        <h1>Welcome, {session.user.email}</h1>
        <p className="subtext">Role: {session.user.role}</p>

        <div className={`panel status ${statusTone}`}>
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
          {tasks.length === 0 ? <li className="task-empty">No tasks yet. Add your first task above.</li> : null}
        </ul>

        <div className="actions">
          <button type="button" onClick={handleSessionExpired}>Logout</button>
        </div>
      </section>
    </main>
  )
}
