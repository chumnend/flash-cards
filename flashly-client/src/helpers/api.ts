import type { IRegisterResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export async function hello(): Promise<{ message: string}> {
    const response = await fetch(`${API_BASE_URL}`);
    if (!response.ok) {
        throw new Error('Something went wrong!')
    }

    return response.json();
}

export async function register(
    firstName: string,
    lastName: string,
    username: string,
    email: string,
    password: string,
): Promise<IRegisterResponse> {
    const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            firstName,
            lastName,
            username,
            email,
            password
        })
    });
    if (!response.ok) {
        throw new Error('Registration failed');
    }

    const data = await response.json();
    return {
        message: data.message,
        user: data.user ? {
            id: data.user.id,
            firstName: data.user.firstName,
            lastName: data.user.lastName,
            username: data.user.username,
            email: data.user.email,
        } : null,
        token: data.token || null,
    }
}
