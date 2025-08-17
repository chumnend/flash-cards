import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import App from './components/app/App';
import ProtectedRoute from './components/common/ProtectedRoute';

import ExplorePage from './components/pages/ExplorePage';
import DeckPage from './components/pages/DeckPage';
import ErrorPage from './components/pages/ErrorPage';

import HomePage from './components/pages/HomePage';
import LoginPage from './components/pages/LoginPage';
import RegisterPage from './components/pages/RegisterPage';

import FeedPage from './components/pages/FeedPage';
import DecksPage from './components/pages/DecksPage';
import ProfilePage from './components/pages/ProfilePage';

import './index.css';
import DeckManager from './components/pages/DeckManager';
import SettingsPage from './components/pages/SettingsPage';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "explore",
        element: <ExplorePage />,
      },
      {
        path: "register",
        element: <RegisterPage />,
      },
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "feed",
        element: (
          <ProtectedRoute>
            <FeedPage />
          </ProtectedRoute>
        ),
      },
      {
        path: "decks",
        element: (
          <ProtectedRoute>
            <DecksPage />
          </ProtectedRoute>
        )
      },
      {
        path: 'decks/:deckId',
        element: <DeckPage />,
      },
      {
        path: 'decks/:deckId/manage',
        element: (
          <ProtectedRoute>
            <DeckManager />
          </ProtectedRoute>
        )
      },
      {
        path: "profile/:userId",
        element: (
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        )
      },
      {
        path: "settings",
        element: (
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        )
      },
    ],
  },
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
