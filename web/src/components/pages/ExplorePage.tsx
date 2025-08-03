import { useEffect, useState } from 'react';

import * as api from '../../helpers/api';

const ExplorePage = () => {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchExplore = async () => {
      const data = await api.explore();
  
      console.log(data);

      setIsLoading(false);
    }
    fetchExplore();
  }, []);

  if (isLoading) {
    return (
      <p>Loading...</p>
    );
  }

  return (
    <div className="explore-page">
      <h1>Explore</h1>
      <p>Discover new flashcard decks and topics.</p>
    </div>
  );
};

export default ExplorePage;
