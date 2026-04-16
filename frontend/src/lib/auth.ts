export type SessionUser = {
  id: number
  email: string
  role: string
}

export type SessionData = {
  token: string
  user: SessionUser
}

const SESSION_KEY = 'primetrade.session'

export function saveSession(data: SessionData): void {
  localStorage.setItem(SESSION_KEY, JSON.stringify(data))
}

export function loadSession(): SessionData | null {
  const raw = localStorage.getItem(SESSION_KEY)
  if (!raw) return null

  try {
    return JSON.parse(raw) as SessionData
  } catch {
    localStorage.removeItem(SESSION_KEY)
    return null
  }
}

export function clearSession(): void {
  localStorage.removeItem(SESSION_KEY)
}
