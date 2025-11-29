import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { useAuthContext } from '../../helpers/context';

const HomePage = () => {
  const { authUser } = useAuthContext();
  const navigate = useNavigate();

  useEffect(() => {
      if (authUser) {
          navigate('/feed');
      }
  }, [authUser, navigate]);

  if (authUser) {
    return null;
  }

  return (
    <div className="home-page">
      <h1>Welcome to Flashly</h1>
      <p>Your ultimate flashcard learning platform!</p>
    </div>
  );
};

export default HomePage;
