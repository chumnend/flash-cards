const BASE_URL = '/api'

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, config)
  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const errorMessage = (data as { error?: string }).error || `Request failed with status ${response.status}`
    throw new Error(errorMessage)
  }

  return data as T
}

export const client = {
  get:    <T>(endpoint: string, options?: RequestInit) =>
            request<T>(endpoint, { method: 'GET', ...options }),
  post:   <T>(endpoint: string, body: unknown, options?: RequestInit) =>
            request<T>(endpoint, { method: 'POST', body: JSON.stringify(body), ...options }),
  put:    <T>(endpoint: string, body: unknown, options?: RequestInit) =>
            request<T>(endpoint, { method: 'PUT', body: JSON.stringify(body), ...options }),
  patch:  <T>(endpoint: string, body: unknown, options?: RequestInit) =>
            request<T>(endpoint, { method: 'PATCH', body: JSON.stringify(body), ...options }),
  delete: <T>(endpoint: string, options?: RequestInit) =>
            request<T>(endpoint, { method: 'DELETE', ...options }),
}
