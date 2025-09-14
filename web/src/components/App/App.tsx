import { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';

import Navbar from '../Navbar/Navbar';
import { type ContextType  } from '../../helpers/context';
import { type IAuthUser } from '../../helpers/types';

import './App.css'

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [authUser, setAuthUser] = useState<IAuthUser | null>(null);

  const createSession = (id: string, name: string, email: string, token: string) => {
    const userSession = {
      id,
      name,
      email,
      token,
      lastLogin: new Date().toISOString(),
    };

    window.localStorage.setItem('userSession', JSON.stringify(userSession));

    setAuthUser({
      id,
      name,
      email,
      token,
    });
    setIsLoggedIn(true);
  };

  const clearSession = () => {
    window.localStorage.removeItem('userSession');
    setAuthUser(null);
    setIsLoggedIn(false);
  };

  useEffect(() => {
    const userSession = localStorage.getItem('userSession');
    if (!userSession) {
      return;
    }

    const parsed = JSON.parse(userSession);
    const { id, name, email, token, lastLogin } = parsed;
    if (!id || !name || !email || !token || !lastLogin) {
      clearSession();
      return;
    }

    const sessionData = { id, name, email, token, lastLogin };    
    if (!sessionData) {
      clearSession();
      return;
    }

    const differenceMs = new Date().getTime() - new Date(sessionData.lastLogin).getTime();
    if (differenceMs > 7.2e6) {  // 2 hours in milliseconds
      clearSession();
      return;
    }

    setAuthUser({
      id: sessionData.id,
      name: sessionData.name,
      email: sessionData.email,
      token: sessionData.token,
    });
    setIsLoggedIn(true);
  }, []);

  const handleRegister = (id: string, name: string, email: string, token: string) => {
    createSession(id, name, email, token);
  };

  const handleLogin = (id: string, name: string, email: string, token: string) => {
    createSession(id, name, email, token);
  };

  const handleLogout = () => {
    clearSession();
  };

  return (
    <div className='app'>
      <Navbar
        isLoggedIn={isLoggedIn}
        authUser={authUser}
        onLogout={handleLogout}
      />

      <main className='app-main'>
        <Outlet context={{ authUser, handleLogin, handleRegister, handleLogout } satisfies ContextType } />
      </main>

      <footer className='app-footer'>
        Nicholas Chumney, 2025
      </footer>
    </div>
  );
};

export default App;
