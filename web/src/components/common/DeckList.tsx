import { useNavigate } from 'react-router-dom'

import type { IDeck } from '../../helpers/types';

import './DeckList.css';

export type Props = {
    decks: Array<IDeck>,
};

const DeckList = (props: Props) => {
    const { decks } = props;

    const navigate = useNavigate();

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
        <div className="decks">
          {deckComponents}
        </div>
    );
}

export default DeckList;
