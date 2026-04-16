import { useEffect, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { clearSession, loadSession } from './lib/auth'
import type { SessionData } from './lib/auth'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { ProtectedRoute } from './router/ProtectedRoute'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1'

export function App() {
  const [session, setSession] = useState<SessionData | null>(() => loadSession())
  const [checkingSession, setCheckingSession] = useState(true)

  useEffect(() => {
    async function validateSession() {
      if (!session) {
        setCheckingSession(false)
        return
      }

      try {
        const response = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            Authorization: `Bearer ${session.token}`,
          },
        })

        if (!response.ok) {
          clearSession()
          setSession(null)
        }
      } catch {
        // Keep existing session on transient network errors.
      } finally {
        setCheckingSession(false)
      }
    }

    void validateSession()
  }, [])

  if (checkingSession) {
    return (
      <main className="shell">
        <section className="card">
          <p className="eyebrow">PrimeTrade Frontend</p>
          <h1>Checking session...</h1>
          <p className="subtext">Validating your access token before loading protected routes.</p>
        </section>
      </main>
    )
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={<LoginPage apiBase={API_BASE} onLogin={setSession} />}
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute session={session}>
              <DashboardPage apiBase={API_BASE} session={session as SessionData} onLogout={() => setSession(null)} />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to={session ? '/dashboard' : '/login'} replace />} />
      </Routes>
    </BrowserRouter>
  )
}
