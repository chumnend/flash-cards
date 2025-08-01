import { useState } from 'react';

import Navbar from './Navbar';

import './App.css';

const App = () => {
  const [username] = useState('Nicholas C.');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
  }

  return (
    <div className='app'>
      <Navbar
        username={username}
        isLoggedIn={isLoggedIn}
        onLogin={handleLogin}
        onLogout={handleLogout}
      />
      <main className='app-main'>
        <h1>Welcome to Flashly</h1>
      </main>
      <footer className='app-footer'>
        Nicholas Chumney, 2025
      </footer>
    </div>
  );
}

export default App;
