import { useNavigate } from 'react-router-dom'

import type { IDeck } from '../../helpers/types';

import './DeckList.css';

export type Props = {
    decks: Array<IDeck>,
    isOwner?: boolean;
};

const DeckList = (props: Props) => {
    const { decks, isOwner } = props;

    const navigate = useNavigate();

    const handleManageClick = (id: string) => {
        navigate(`/decks/${id}/manage`);
    }

    const handleViewClick = (id: string) => {
        navigate(`/decks/${id}`);
    }

    if (decks.length === 0) {
        return (
            <div className="decks-not-found">
                <p>No decks were found.</p>
            </div>
        )
    }

    const deckComponents = decks.map(deck => (
        <div key={deck.id} className="deck">
            <h2 className='deck-title'>{deck.name}</h2>
            <p className='deck-owner'>By {deck.owner}</p>
            <p className='deck-description'>{deck.description}</p>
            <p className='deck-rating'>{`${deck.rating} / 5.0`}</p>
            <p className='deck-categories'>{deck.categories.join(', ')}</p>
            <div className='deck-btns'>
                {isOwner && <button onClick={() => handleManageClick(deck.id)}>Manage</button>}
                <button onClick={() => handleViewClick(deck.id)}>View</button>
            </div>
        </div>
    ));

    return (
        <div className="decks">
          {deckComponents}
        </div>
    );
}

export default DeckList;
