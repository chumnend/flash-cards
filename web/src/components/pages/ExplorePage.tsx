import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'

import * as api from '../../helpers/api';
import type { IDeck } from '../../helpers/types';

import './ExplorePage.css';

const ExplorePage = () => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [decks, setDecks] = useState<IDeck[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchExplore = async () => {
      const data = await api.explore();

      setDecks(data.decks);
      setIsLoading(false);
    }
    fetchExplore();
  }, []);

  const handleViewClick = (id: string) => {
    navigate(`/decks/:${id}`);
  }

  const deckComponents = decks.map(deck => (
    <div key={deck.id} className="deck">
      <h2 className='deck-title'>{deck.name}</h2>
      <p className='deck-owner'>By {deck.owner}</p>
      <p className='deck-description'>{deck.description}</p>
      <div className='deck-btns'>
        <button onClick={() => handleViewClick(deck.id)}>View</button>
      </div>
    </div>
  ));

  return (
    <div className="explore-page">
      <h1>Explore</h1>
      <p>Discover new flashcard decks and topics.</p>
      {isLoading ? <p className="loader">Loading...</p> : (
        <div className="decks-container">
          {deckComponents}
        </div>
      )}
    </div>
  );
};

export default ExplorePage;
