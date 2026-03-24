import { useEffect } from "react";
import { useNavigate } from 'react-router-dom';

import Page from "../../layout/Page";
import { useAuth } from '../../providers/AuthProvider';

import './HomePage.css';

const HomePage = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
      if (auth.isAuthenticated) {
          navigate('/feed');
      }
  }, [auth.isAuthenticated, navigate]);

  if (auth.isAuthenticated) {
    return null;
  }

  return (
    <Page>
      <div className="homepage-hero">
        <h1>Welcome to Flashly</h1>
        <p>Your ultimate flashcard learning platform!</p>
      </div>
    </Page>
  );
}

export default HomePage
