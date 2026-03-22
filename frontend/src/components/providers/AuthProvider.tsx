import React, { createContext, useContext, useState } from 'react';

import { loginUser } from '../../helpers/api/auth'
import type { LoginPayload, User } from '../../helpers/types';

interface AuthContextProps {
    user: User | null,
    token: string | null,
    isAuthenticated: boolean,
    login(payload: LoginPayload): Promise<void>,
    logout(): void,
}

export const AuthContext = createContext<AuthContextProps>({
    user: null,
    token: null,
    isAuthenticated: false,
    login: async () => {},
    logout: () => {},
});

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: React.ReactNode,
}

const AuthProvider = (props: AuthProviderProps) => {
    const [user, setUser] = useState<User | null>(() => {
        const stored = window.localStorage.getItem('flashly_user');
        return stored ? JSON.parse(stored) : null;
    });
    const [token, setToken] = useState<string | null>(() => {
        return window.localStorage.getItem('flashly_token');
    });

    const login = async (payload: LoginPayload) => {
        try {
            const { user, token } = await loginUser(payload);
            setUser(user);
            setToken(token);
            window.localStorage.setItem('flashly_token', token);
            window.localStorage.setItem('flashly_user', JSON.stringify(user));
        } catch (error) {
            // Clean up any partial state
            setUser(null);
            setToken(null);
            throw error;
        }
    }

    const logout = () => {
        setUser(null);
        setToken(null);
        window.localStorage.removeItem('flashly_token');
        window.localStorage.removeItem('flashly_user');
    }

    const contextValue = {
        user,
        token,
        isAuthenticated: !!user && !!token,
        login,
        logout
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {props.children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;
