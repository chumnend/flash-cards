import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import type { ICard, IDeck } from '../../helpers/types';

import './DeckManager.css';

const DeckManager = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [deck, setDeck] = useState<IDeck | null>(null)
    const [cards, setCards] = useState<Array<ICard>>([]);

    const params = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDeck = async () => {
            try {
                if (!params.deckId) {
                    throw new Error('Deck ID is missing');
                }
                const data = await api.deck(params.deckId);
                if(!data) {
                    throw new Error('Deck not found');
                }
                setDeck(data.deck);
                setCards(data.deck.cards);
                setIsLoading(false);
            } catch {
                setIsLoading(false);
                navigate('error');
            }
        }
        fetchDeck();
    }, [params.deckId, navigate]);

    if (isLoading) return <Loader />

    const areCards = cards.length > 0;

    const totalCards = cards.length;

    const cardsComponent = (
        <div className="deck-manager-cards">
            {cards.map(card => (
                <div key={card.id} className="deck-manager-card">
                    <p>{card?.frontText} || {card?.backText}</p>
                    <div>
                        <button>Modify</button>
                        <button>Delete</button>
                    </div>
                </div>
            ))}
        </div>
    );

    const noCardsComponent = (
        <p>No cards are currently in this deck.</p>
    );

    return (
        <div className="deck-manager">
            <div className="deck-manager-header">
                <div>
                    <h2>{deck?.name}</h2>
                    <p>{deck?.description}</p>
                    <p>Number of Cards: {totalCards}</p>
                </div>
                <div>
                    <button>View</button>
                    <button>Delete</button>
                </div>
            </div>

            <div className="deck-manager-content">
                <button>Create New Card</button>
                {areCards ? cardsComponent : noCardsComponent}
            </div>
        </div>
    );
}

export default DeckManager;
