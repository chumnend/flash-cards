import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import DeckList from '../common/DeckList';
import Loader from '../common/Loader';
import Modal from '../common/Modal';
import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';
import type { IDeck } from '../../helpers/types';

import './DecksPage.css';

const DecksPage = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [decks, setDecks] = useState<IDeck[]>([]);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [isFormSubmitting, setIsFormSubmitting] = useState<boolean>(false);
    const [formData, setFormData] = useState<{[key: string]: string}>({
        name: '',
        description: '',
    });
    const [formErrors, setFormErrors] = useState<{[key: string]: string}>({});
    const { authUser } = useAuthContext();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDecks = async () => {
            if (!authUser?.token) {
                setIsLoading(false);
                return;
            }
            const data = await api.decks(authUser.token);
            setDecks(data.decks);
            setIsLoading(false);
        }
        fetchDecks();
    }, [authUser]);

    const handleNewDeckClick = () => {
        setIsModalOpen(true);
    }
    
    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value,
        }));
    }

    const validateForm = (): boolean => {
        const newErrors: {[key: string]: string} = {};

        if (!formData.name.trim()) {
            newErrors.name = 'Deck name is required';
        }

        setFormErrors(newErrors);

        return Object.keys(newErrors).length === 0;
    }

    const handleFormSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        setIsFormSubmitting(true);

        try {
            const data = await api.newDeck(formData.name, formData.description);
            navigate(`/decks/${data.deck.id}/manage`);
        } catch (error) {
            console.error('New deck submission failed', error);
        } finally {
            setIsFormSubmitting(false);
        }
    }

    const newDeckModal = (
        <Modal
            title="Create a new deck"
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
        >
            <form className="new-deck-form" onSubmit={handleFormSubmit}>
                <div className="form-group">
                    <label htmlFor="name">Deck Name:</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={formData.name}
                        onChange={handleFormChange}
                        className={formErrors.name ? 'error' : ''}
                        placeholder="Enter new deck name"
                    />
                    {formErrors.name && <span className="error-message">{formErrors.name}</span>}
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description:</label>
                    <input
                        type="text"
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleFormChange}
                        placeholder="Enter description of this deck"
                    />
                </div>

                <button 
                    type="submit" 
                    className="submit-button"
                    disabled={isFormSubmitting}
                >
                    {isFormSubmitting ? 'Creating...' : 'Create'}
                </button>
            </form>
        </Modal>
    );

    return (
        <div className="decks-page">
            <div className="decks-header">
                <div>
                    <h1>My Decks</h1>
                    <p>Manage your flashcard decks here.</p>
                </div>
                <button onClick={handleNewDeckClick}>+ New Deck</button>
            </div>
            {isLoading ? <Loader /> : <DeckList decks={decks} isOwner />}
            {newDeckModal}
        </div>
    );
};

export default DecksPage;
