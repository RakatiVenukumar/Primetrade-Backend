import { Navigate } from 'react-router-dom'
import type { SessionData } from '../lib/auth'

type ProtectedRouteProps = {
  session: SessionData | null
  children: JSX.Element
}

export function ProtectedRoute({ session, children }: ProtectedRouteProps) {
  if (!session) {
    return <Navigate to="/login" replace />
  }

  return children
}
