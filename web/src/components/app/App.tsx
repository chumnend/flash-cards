import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import Navbar from './Navbar';

import './App.css'

const App = () => {
  const [username] = useState('Nicholas C.');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogout = () => {
    setIsLoggedIn(false);
  }

  return (
    <div className='app'>
      <Navbar
        username={username}
        isLoggedIn={isLoggedIn}
        onLogout={handleLogout}
      />

      <main className='app-main'>
        <Outlet />
      </main>

      <footer className='app-footer'>
        Nicholas Chumney, 2025
      </footer>
    </div>
  );
};

export default App;
