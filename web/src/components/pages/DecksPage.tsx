import { useEffect, useState } from 'react';

import DeckList from '../common/DeckList';
import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';
import type { IDeck } from '../../helpers/types';

import './DecksPage.css';

const DecksPage = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [decks, setDecks] = useState<IDeck[]>([]);
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

    return (
        <div className="decks-page">
          <h1>My Decks</h1>
          <p>Manage your flashcard decks here.</p>
            {isLoading ? <Loader /> : <DeckList decks={decks} isOwner />}
        </div>
    );
};

export default DecksPage;
