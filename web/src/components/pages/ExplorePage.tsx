import { useEffect, useState } from 'react';

import DeckList from '../common/DeckList';
import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import type { IDeck } from '../../helpers/types';

import './ExplorePage.css';

const ExplorePage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [decks, setDecks] = useState<IDeck[]>([]);

  useEffect(() => {
    const fetchExplore = async () => {
      const data = await api.explore();
      setDecks(data.decks);
      setIsLoading(false);
    }
    fetchExplore();
  }, []);

  return (
    <div className="explore-page">
      <h1>Explore</h1>
      <p>Discover new flashcard decks and topics.</p>
      {isLoading ? <Loader /> : <DeckList decks={decks} />}
    </div>
  );
};

export default ExplorePage;
