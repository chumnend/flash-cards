import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

import Loader from '../Loader'
import Modal from '../Modal/Modal';
import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';
import type { ICard, IDeck } from '../../helpers/types';

import './DeckManagerPage.css';

const DeckManagerPage = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [deck, setDeck] = useState<IDeck | null>(null)
    const [isDeckDeleteModalOpen, setIsDeckDeleteModalOpen] = useState<boolean>(false);
    const [isDeckDeleting, setIsDeckDeleting] = useState<boolean>(false);
    const [cards, setCards] = useState<Array<ICard>>([]);
    const [isCardModalOpen, setIsCardModalOpen] = useState<boolean>(false);
    const [isCardFormSubmitting, setIsCardFormSubmitting] = useState<boolean>(false);
    const [editingCardId, setEditingCardId] = useState<string | null>(null);
    const [cardFormData, setCardFormData] = useState<{[key: string]: string}>({
        frontText: '',
        backText: '',
    });
    const [isCardDeleteModalOpen, setIsCardDeleteModalOpen] = useState<boolean>(false);
    const [cardToDelete, setCardToDelete] = useState<string | null>(null);
    const [isCardDeleting, setIsCardDeleting] = useState<boolean>(false);
    const { authUser } = useAuthContext();
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

    const handleDeckViewClick = () => {
        if (deck) {
            navigate(`/decks/${deck.id}`);
        }
    }

    const handleDeckDeleteClick = () => {
        setIsDeckDeleteModalOpen(true);
    }

    const handleNewCardClick = () => {
        setEditingCardId(null);
        clearCardFormData();
        setIsCardModalOpen(true);
    }

    const handleModifyCardClick = (id: string) => {
        const cardToModify = cards.find(card => card.id === id);
        if (cardToModify) {
            setEditingCardId(id);
            setCardFormData({
                frontText: cardToModify.frontText,
                backText: cardToModify.backText,
            });
            setIsCardModalOpen(true);
        }
    }

    const handleDeleteCardClick = (id: string) => {
        setCardToDelete(id);
        setIsCardDeleteModalOpen(true);
    }

    const handleCardFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setCardFormData(prev => ({
            ...prev,
            [name]: value,
        }));
    }

    const clearCardFormData = () => {
        setCardFormData({
            frontText: '',
            backText: '',
        });
        setEditingCardId(null);
    }

    const handleCardSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        setIsCardFormSubmitting(true);

        try {
            if (!authUser?.token) {
                throw new Error('Authentication required');
            }
            if (editingCardId) {
                const data = await api.modifyCard(deck!.id, editingCardId, cardFormData.frontText, cardFormData.backText, authUser.token);
                setCards(prev => prev.map(card => 
                    card.id === editingCardId ? data.card : card
                ));
                clearCardFormData();
                setIsCardModalOpen(false);
            } else {
                const data = await api.newCard(cardFormData.frontText, cardFormData.backText, deck!.id, authUser.token);
                clearCardFormData();
                setCards(prev => [...prev, data.card]);
                setIsCardModalOpen(false);
            }
        } catch(error) {
            console.error('Unable to create card', error);
        } finally {
            setIsCardFormSubmitting(false);
        }
    }

    const handleConfirmDeckDelete = async () => {
        if (!deck) return;

        setIsDeckDeleting(true);
        try {
            if (!authUser?.token) {
                throw new Error('Authentication required');
            }
            await api.deleteDeck(deck.id, authUser.token);
            // Navigate back to decks page after successful deletion
            navigate('/decks');
        } catch (error) {
            console.error('Unable to delete deck', error);
        } finally {
            setIsDeckDeleting(false);
            setIsDeckDeleteModalOpen(false);
        }
    }

    const handleCancelDeckDelete = () => {
        setIsDeckDeleteModalOpen(false);
    }

    const handleConfirmCardDelete = async () => {
        if (!cardToDelete) return;

        setIsCardDeleting(true);
        try {
            if (!authUser?.token || !deck) {
                throw new Error('Authentication required');
            }
            await api.deleteCard(deck.id, cardToDelete, authUser.token);
            setCards(prev => prev.filter(card => card.id !== cardToDelete));
        } catch (error) {
            console.error('Unable to delete card', error);
        } finally {
            setIsCardDeleting(false);
            setIsCardDeleteModalOpen(false);
            setCardToDelete(null);
        }
    }

    const handleCancelCardDelete = () => {
        setIsCardDeleteModalOpen(false);
        setCardToDelete(null);
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

    return (
        <div className="deck-manager">
            <div className="deck-manager-header">
                <div>
                    <h2>{deck?.name}</h2>
                    <p>{deck?.description}</p>
                    <p>Number of Cards: {totalCards}</p>
                </div>
                <div>
                    <button onClick={handleDeckViewClick}>View</button>
                    <button onClick={handleDeckDeleteClick}>Delete</button>
                </div>
            </div>

            <div className="deck-manager-content">
                <button onClick={handleNewCardClick}>Create New Card</button>
                {areCards ? cardsComponent : noCardsComponent}
            </div>

            {/* Card Modal */}
            <Modal
                title={editingCardId ? "Modify card" : "Create a new card"}
                isOpen={isCardModalOpen}
                onClose={() => {
                    setIsCardModalOpen(false);
                    clearCardFormData();
                }}
            >
                {isCardFormSubmitting ? (
                    <div className="card-loader">
                        <Loader />
                    </div>
                ) : (
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
                            <button type="submit">{editingCardId ? "Modify" : "Create"}</button>
                        </form>
                )}

            </Modal>

            {/* Deck Delete Confirmation Modal */}
            <Modal
                title="Confirm Deck Deletion"
                isOpen={isDeckDeleteModalOpen}
                onClose={handleCancelDeckDelete}
            >
                {isDeckDeleting ? (
                    <div className="delete-loader">
                        <Loader />
                    </div>
                ) : (
                    <div className="delete-confirmation">
                        <p>Are you sure you want to delete "{deck?.name}"?</p>
                        <p>This action cannot be undone and will permanently delete the deck and all its cards.</p>
                        <div className="delete-actions">
                            <button 
                                onClick={handleCancelDeckDelete}
                                className="cancel-button"
                            >
                                Cancel
                            </button>
                            <button 
                                onClick={handleConfirmDeckDelete}
                                className="delete-button"
                            >
                                Delete Deck
                            </button>
                        </div>
                    </div>
                )}
            </Modal>

            {/* Card Delete Confirmation Modal */}
            <Modal
                title="Confirm Card Deletion"
                isOpen={isCardDeleteModalOpen}
                onClose={handleCancelCardDelete}
            >
                {isCardDeleting ? (
                    <div className="delete-loader">
                        <Loader />
                    </div>
                ) : (
                    <div className="delete-confirmation">
                        <p>Are you sure you want to delete this card?</p>
                        <p>This action cannot be undone.</p>
                        <div className="delete-actions">
                            <button 
                                onClick={handleCancelCardDelete}
                                className="cancel-button"
                            >
                                Cancel
                            </button>
                            <button 
                                onClick={handleConfirmCardDelete}
                                className="delete-button"
                            >
                                Delete Card
                            </button>
                        </div>
                    </div>
                )}
            </Modal>
        </div>
    );
}

export default DeckManagerPage;
