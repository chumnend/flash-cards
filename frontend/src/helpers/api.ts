const API_BASE_URL = '/api'

type ApiStatusResponse = {
  message: string
  status: string
  timestamp: string
}

export async function checkApiStatus(): Promise<ApiStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/status`)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  const data = await response.json()

  return {
    message: data.message,
    status: data.status,
    timestamp: data.timestamp,
  }
}

type User = {
  id: string
  firstName: string
  lastName: string
  username: string
  email: string
}

type AuthResponse = {
  message: string
  user: User
  token: string
}

type RegisterPayload = {
  firstName: string
  lastName: string
  username: string
  email: string
  password: string
}

export async function registerUser(payload: RegisterPayload): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  const data = await response.json()

  if (!response.ok) {
    const errorMessage = (data && data.error) || `Request failed with status ${response.status}`
    throw new Error(errorMessage)
  }

  return data as AuthResponse
}

type LoginPayload = {
  email: string
  password: string
}

export async function loginUser(payload: LoginPayload): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  const data = await response.json()

  if (!response.ok) {
    const errorMessage = (data && data.error) || `Request failed with status ${response.status}`
    throw new Error(errorMessage)
  }

  return data as AuthResponse
}
