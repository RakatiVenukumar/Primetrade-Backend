import { useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { loadSession } from './lib/auth'
import type { SessionData } from './lib/auth'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { ProtectedRoute } from './router/ProtectedRoute'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1'

export function App() {
  const [session, setSession] = useState<SessionData | null>(() => loadSession())

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
