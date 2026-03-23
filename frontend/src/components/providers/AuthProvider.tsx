import React, { createContext, useContext, useState } from 'react';

import { loginUser } from '../../helpers/api/auth';
import type { LoginPayload, User } from '../../helpers/types';

const STORAGE_KEYS = {
    token: 'flashly_token',
    user: 'flashly_user',
} as const;

interface AuthContextProps {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    login(payload: LoginPayload): Promise<void>;
    logout(): void;
}

export const AuthContext = createContext<AuthContextProps | null>(null);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: React.ReactNode;
}

const AuthProvider = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<User | null>(() => {
        try {
            const stored = window.localStorage.getItem(STORAGE_KEYS.user);
            return stored ? JSON.parse(stored) : null;
        } catch {
            window.localStorage.removeItem(STORAGE_KEYS.user);
            return null;
        }
    });

    const [token, setToken] = useState<string | null>(
        () => window.localStorage.getItem(STORAGE_KEYS.token)
    );

    const login = async (payload: LoginPayload) => {
        try {
            const { user, token } = await loginUser(payload);
            window.localStorage.setItem(STORAGE_KEYS.token, token);
            window.localStorage.setItem(STORAGE_KEYS.user, JSON.stringify(user));
            setUser(user);
            setToken(token);
        } catch (error) {
            window.localStorage.removeItem(STORAGE_KEYS.token);
            window.localStorage.removeItem(STORAGE_KEYS.user);
            setUser(null);
            setToken(null);
            throw error;
        }
    };

    const logout = () => {
        window.localStorage.removeItem(STORAGE_KEYS.token);
        window.localStorage.removeItem(STORAGE_KEYS.user);
        setUser(null);
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{
            user,
            token,
            isAuthenticated: !!user && !!token,
            login,
            logout,
        }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
