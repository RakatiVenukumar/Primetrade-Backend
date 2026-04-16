export class ApiError extends Error {
  status: number
  details?: unknown

  constructor(message: string, status: number, details?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

function buildHeaders(token?: string, includeJson = true): HeadersInit {
  const headers: HeadersInit = {}

  if (includeJson) {
    headers['Content-Type'] = 'application/json'
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  return headers
}

export async function apiRequest<T>(
  url: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...buildHeaders(token, options.body !== undefined),
      ...(options.headers ?? {}),
    },
  })

  const raw = await response.text()
  const parsed = raw ? JSON.parse(raw) : null

  if (!response.ok) {
    const fallback = `Request failed with status ${response.status}`
    const message = parsed?.error?.message ?? parsed?.detail ?? fallback
    throw new ApiError(message, response.status, parsed)
  }

  return parsed as T
}

export async function apiRequestNoContent(
  url: string,
  options: RequestInit = {},
  token?: string
): Promise<void> {
  await apiRequest<unknown>(url, options, token)
}
