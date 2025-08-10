import { useEffect, useState } from 'react';

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
    const { authUser } = useAuthContext();

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

    const newDeckModal = (
        <Modal
            title="Create a new deck"
            isOpen={isModalOpen}
            onClose={() => setIsModalOpen(false)}
        >
            testing...
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
