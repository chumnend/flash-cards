import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'

import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';
import type { IDeck } from '../../helpers/types';

import './FeedPage.css';

const FeedPage = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [decks, setDecks] = useState<IDeck[]>([]);
    const { authUser } = useAuthContext();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchFeed = async () => {
            if (!authUser?.token) {
                setIsLoading(false);
                return;
            }
            const data = await api.feed(authUser.token);

            setDecks(data.decks);
            setIsLoading(false);
        }
        fetchFeed();
    }, [authUser]);

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
        <div className="feed-page">
            <h1>Your Feed</h1>
            <p>See your friends flashcard decks.</p>
            {isLoading ? <p className="loader">Loading...</p> : (
                <div className="decks-container">
                    {deckComponents}
                </div>
            )}
        </div>
    );
}

export default FeedPage;
