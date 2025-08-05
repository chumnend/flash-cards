import { useEffect, useState } from 'react';

import DeckList from '../common/DeckList';
import Loader from '../common/Loader';
import * as api from '../../helpers/api';
import { useAuthContext } from '../../helpers/context';
import type { IDeck } from '../../helpers/types';

import './FeedPage.css';

const FeedPage = () => {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [decks, setDecks] = useState<IDeck[]>([]);
    const { authUser } = useAuthContext();

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

    return (
        <div className="feed-page">
            <h1>Your Feed</h1>
            <p>See your friends flashcard decks.</p>
            {isLoading ? <Loader /> : <DeckList decks={decks} />}
        </div>
    );
}

export default FeedPage;
