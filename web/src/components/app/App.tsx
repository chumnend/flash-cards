import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import Navbar from './Navbar';
import { type ContextType  } from '../../helpers/context';
import { type IAuthUser } from '../../helpers/types';

import './App.css'

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [authUser, setAuthUser] = useState<IAuthUser | null>(null);

  const handleRegister = (id: string, name: string, email: string, token: string) => {
      setIsLoggedIn(true);
      setAuthUser({
        id,
        name,
        email,
        token,
      });
  }

  const handleLogin = (id: string, name: string, email: string, token: string) => {
      setIsLoggedIn(true);
      setAuthUser({
        id,
        name,
        email,
        token,
      });
  }

  const handleLogout = () => {
    setIsLoggedIn(false);
    setAuthUser(null);
  }

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
