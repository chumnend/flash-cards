import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

import Loader from '../common/Loader';
import Modal from '../common/Modal';
import * as api from '../../helpers/api';
import type { ICard, IDeck } from '../../helpers/types';

import './DeckManager.css';

const DeckManager = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [deck, setDeck] = useState<IDeck | null>(null)
    const [cards, setCards] = useState<Array<ICard>>([]);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [isCardFormSubmitting, setIsCardFormSubmitting] = useState<boolean>(false);
    const [cardFormData, setCardFormData] = useState<{[key: string]: string}>({
        frontText: '',
        backText: '',
    });
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

    const handleNewCardClick = () => {
        setIsModalOpen(true);
    }

    const handleModifyCardClick = (id: string) => {
        alert(`modifying card with id: ${id}`)
        setIsModalOpen(true);  
    }

    const handleDeleteCardClick = (id: string) => {
        alert(`deleting card with id: ${id}`)
    }

    const handleCardFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setCardFormData(prev => ({
            ...prev,
            [name]: value,
        }));
    }

    const handleCardSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        setIsCardFormSubmitting(true);

        try {
            alert('submitting...');
        } catch(error) {
            console.error('Unable to create card', error);
        } finally {
            setIsCardFormSubmitting(false);
        }
    }

    if (isLoading) return <Loader />

    const areCards = cards.length > 0;

    const totalCards = cards.length;

    const cardsComponent = (
        <div className="deck-manager-cards">
            {cards.map(card => (
                <div key={card.id} className="deck-manager-card">
                    <p>{card?.frontText} || {card?.backText}</p>
                    <div>
                        <button onClick={() => handleModifyCardClick(card.id)}>Modify</button>
                        <button onClick={() => handleDeleteCardClick(card.id)}>Delete</button>
                    </div>
                </div>
            ))}
        </div>
    );

    const noCardsComponent = (
        <p>No cards are currently in this deck.</p>
    );

    const cardModal = (
        <Modal
            title="Create a new card"
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
        >
            {isCardFormSubmitting ? <Loader /> : (
                <form className="card-form" onSubmit={handleCardSubmit}>
                        <div className='form-group'>
                            <label htmlFor='frontText'>Front Card Text</label>
                            <input 
                                type="text"
                                id="frontText"
                                name="frontText"
                                value={cardFormData.frontText}
                                onChange={handleCardFormChange}
                                placeholder='Text on front side of card'
                            />
                        </div>
                        <div className='form-group'>
                            <label htmlFor='backText'>Back Card Text</label>
                            <input 
                                type="text"
                                id="backText"
                                name="backText"
                                value={cardFormData.backText}
                                onChange={handleCardFormChange}
                                placeholder='Text on back side of card'
                            />
                        </div>
                        <button type="submit">Create</button>
                    </form>
            )}

        </Modal>
    )

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
                <button onClick={handleNewCardClick}>Create New Card</button>
                {areCards ? cardsComponent : noCardsComponent}
            </div>

            {cardModal}
        </div>
    );
}

export default DeckManager;
