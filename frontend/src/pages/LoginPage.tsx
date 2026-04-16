import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { saveSession } from '../lib/auth'
import type { SessionData } from '../lib/auth'

type LoginResponse = {
  access_token: string
  token_type: string
  user: {
    id: number
    email: string
    role: string
  }
}

type LoginPageProps = {
  apiBase: string
  onLogin: (session: SessionData) => void
}

export function LoginPage({ apiBase, onLogin }: LoginPageProps) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('step8user@example.com')
  const [password, setPassword] = useState('Step8Pass123')
  const [status, setStatus] = useState('Ready')
  const [tokenPreview, setTokenPreview] = useState('No token yet')

  const canSubmit = useMemo(() => email.length > 0 && password.length > 0, [email, password])

  async function handleLogin(event: FormEvent) {
    event.preventDefault()
    setStatus('Authenticating...')

    try {
      const response = await fetch(`${apiBase}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        setStatus(`Login failed: ${body?.error?.message ?? 'unknown error'}`)
        return
      }

      const data = (await response.json()) as LoginResponse
      const session = { token: data.access_token, user: data.user }
      saveSession(session)
      onLogin(session)
      setTokenPreview(`${data.access_token.slice(0, 24)}...`)
      setStatus(`Logged in as ${data.user.email} (${data.user.role})`)
      navigate('/dashboard', { replace: true })
    } catch {
      setStatus('Network error while calling backend API')
    }
  }

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">PrimeTrade Frontend</p>
        <h1>Auth Gateway</h1>
        <p className="subtext">Step 16: Protected routes and persistent auth session.</p>

        <form onSubmit={handleLogin} className="grid">
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
          </label>

          <label>
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
          </label>

          <button type="submit" disabled={!canSubmit}>Login</button>
        </form>

        <div className="panel">
          <p><strong>API:</strong> {apiBase}</p>
          <p><strong>Status:</strong> {status}</p>
          <p><strong>Token:</strong> {tokenPreview}</p>
        </div>
      </section>
    </main>
  )
}
