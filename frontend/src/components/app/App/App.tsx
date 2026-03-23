import { Route, Routes } from 'react-router-dom'

import Header from '../../layout/Header'
import Footer from '../../layout/Footer'
import ProtectedRoute from '../ProtectedRoute'

import HomePage from '../../pages/HomePage'
import LoginPage from '../../pages/LoginPage'
import RegisterPage from '../../pages/RegisterPage'
import NotFoundPage from '../../pages/NotFoundPage'
import ExplorePage from '../../pages/ExplorePage'
import FeedPage from '../../pages/FeedPage'
import DecksPage from '../../pages/DecksPage'
import DeckPage from '../../pages/DeckPage'
import DeckManagerPage from '../../pages/DeckManagerPage'
import ProfilePage from '../../pages/ProfilePage'
import SettingsPage from '../../pages/SettingsPage'

const App = () => {
  return (
    <div className='app'>
      <Header />
      <div className='app-main'>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/decks/:deckId" element={<DeckPage />} />
        
          {/* Protected routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/feed" element={<FeedPage />} />
            <Route path="/decks" element={<DecksPage />} />
            <Route path="/decks/:deckId/manage" element={<DeckManagerPage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </div>
      <Footer />
    </div>
  )
}

export default App
