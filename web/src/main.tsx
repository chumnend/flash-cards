import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import App from './components/App';
import ProtectedRoute from './components/ProtectedRoute';

import ExplorePage from './components/ExplorePage';
import DeckPage from './components/DeckPage';
import ErrorPage from './components/ErrorPage';

import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';

import FeedPage from './components/FeedPage/FeedPage';
import DecksPage from './components/DecksPage/DecksPage';
import ProfilePage from './components/ProfilePage/ProfilePage';

import './index.css';
import DeckManagerPage from './components/DeckManagerPage';
import SettingsPage from './components/SettingsPage';

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
            <DeckManagerPage />
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
