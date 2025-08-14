import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import type { ICard, IDeck } from '../../helpers/types';

import './DeckPage.css';

const Deck = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [deck, setDeck] = useState<IDeck | null>(null)
    const [cards, setCards] = useState<Array<ICard>>([]);
    const [currentCard, setCurrentCard] = useState<ICard | null>(null);
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const [showFace, setShowFace] = useState<boolean>(true);

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
                setCurrentCard(data.deck.cards[0]);
                setCurrentIndex(0);
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

    const updateSlide = (n: number) => {
        let newIndex = currentIndex + n;
        if (newIndex >= totalCards) {
            newIndex = 0;
        }
        if (newIndex < 0) {
            newIndex = totalCards - 1;
        }
        setCurrentCard(cards[newIndex]);
        setCurrentIndex(newIndex);
        setShowFace(true);
    }

    const flipCard = () => {
        setShowFace(prev => !prev);
    }

    const slideshowComponent = (
        <div className='slideshow'>
            <div className="slideshow-cards">
                <div className='card' onClick={flipCard}>
                    <div className='card-frame'>
                        {showFace ? (
                            <div className='card-face card-front'>
                                <span className='card-face-extra'>front</span>
                                <span className='card-face-text'>{currentCard ? currentCard.frontText : ''}</span>
                                <span className='card-face-extra'>click/tap to flip</span>
                            </div>
                        ) : (
                            <div className='card-face card-back'>
                                <span className='card-face-extra'>back</span>
                                <span className='card-face-text'>{currentCard ? currentCard.backText : ''}</span>
                                <span className='card-face-extra'>click/tap to flip</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <div className="slideshow-controls">
                <button onClick={() => updateSlide(-1)}>&#10094;</button>
                    <span className='slide-index'>
                        <span>{currentIndex + 1} / {deck?.cards.length}</span>
                    </span>
                <button onClick={() => updateSlide(1)}>&#10095;</button>
            </div>
        </div>
    );

    return (
        <div className="deck-page">
            {areCards ? slideshowComponent : <p>No cards are currently in this deck.</p>}
        </div>
    );
}

export default Deck;
