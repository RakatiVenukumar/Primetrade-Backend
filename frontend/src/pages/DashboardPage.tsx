import { useNavigate } from 'react-router-dom'
import type { SessionData } from '../lib/auth'
import { clearSession } from '../lib/auth'

type DashboardPageProps = {
  apiBase: string
  session: SessionData
  onLogout: () => void
}

export function DashboardPage({ apiBase, session, onLogout }: DashboardPageProps) {
  const navigate = useNavigate()

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
        </div>

        <div className="actions">
          <button type="button" onClick={handleLogout}>Logout</button>
        </div>
      </section>
    </main>
  )
}
