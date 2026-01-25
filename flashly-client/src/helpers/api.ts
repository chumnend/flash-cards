const API_BASE_URL = 'http://localhost:8080';

export async function hello(): Promise<{ message: string}> {
    const response = await fetch(`${API_BASE_URL}`);
    if (!response.ok) {
        throw new Error('Something went wrong!')
    }

    return response.json();
}
