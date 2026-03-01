const API_BASE_URL = '/api';

export async function checkApiStatus(): Promise<{ message: string, status: string, timestamp: string }> {
  const response = await fetch(`${API_BASE_URL}/status`)
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  const data = await response.json();

  return {
    message: data.message,
    status: data.status,
    timestamp: data.timestamp,
  }
}
