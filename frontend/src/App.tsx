import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'

type LoginResponse = {
  access_token: string
  token_type: string
  user: {
    id: number
    email: string
    role: string
  }
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1'

export function App() {
  const [email, setEmail] = useState('step8user@example.com')
  const [password, setPassword] = useState('Step8Pass123')
  const [token, setToken] = useState('')
  const [status, setStatus] = useState('Ready')

  const tokenPreview = useMemo(() => {
    if (!token) return 'No token yet'
    return `${token.slice(0, 24)}...`
  }, [token])

  async function handleLogin(event: FormEvent) {
    event.preventDefault()
    setStatus('Authenticating...')

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
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
      setToken(data.access_token)
      setStatus(`Logged in as ${data.user.email} (${data.user.role})`)
    } catch {
      setStatus('Network error while calling backend API')
    }
  }

  return (
    <main className="shell">
      <section className="card">
        <p className="eyebrow">PrimeTrade Frontend</p>
        <h1>Auth Gateway</h1>
        <p className="subtext">Step 15 kickoff: React client connected to FastAPI backend.</p>

        <form onSubmit={handleLogin} className="grid">
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
          </label>

          <label>
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
          </label>

          <button type="submit">Login</button>
        </form>

        <div className="panel">
          <p><strong>API:</strong> {API_BASE}</p>
          <p><strong>Status:</strong> {status}</p>
          <p><strong>Token:</strong> {tokenPreview}</p>
        </div>
      </section>
    </main>
  )
}
