from flashly.models import DeckModel

def serialize_single_deck_tuple(deck_tuple):
    """
    Sérialise un tuple de données de deck en format JSON.
    Gère différents formats de tuples selon la requête SQL.
    """
    if len(deck_tuple) == 8:
        # Format pour explore_decks et feed_decks (sans publish_status et owner_id)
        return {
            'id': str(deck_tuple[0]),
            'name': deck_tuple[1],
            'description': deck_tuple[2],
            'rating': float(deck_tuple[3]),
            'created_at': deck_tuple[4].isoformat() if deck_tuple[4] else None,
            'updated_at': deck_tuple[5].isoformat() if deck_tuple[5] else None,
            'owner': deck_tuple[6],
            'card_count': int(deck_tuple[7])
        }
    elif len(deck_tuple) == 9:
        # Format pour find_decks_by_user_id (avec publish_status)
        return {
            'id': str(deck_tuple[0]),
            'name': deck_tuple[1],
            'description': deck_tuple[2],
            'publish_status': deck_tuple[3],
            'rating': float(deck_tuple[4]),
            'created_at': deck_tuple[5].isoformat() if deck_tuple[5] else None,
            'updated_at': deck_tuple[6].isoformat() if deck_tuple[6] else None,
            'owner': deck_tuple[7],
            'card_count': int(deck_tuple[8])
        }
    elif len(deck_tuple) == 10:
        # Format pour find_deck_by_id (avec publish_status et owner_id)
        return {
            'id': str(deck_tuple[0]),
            'name': deck_tuple[1],
            'description': deck_tuple[2],
            'publish_status': deck_tuple[3],
            'owner_id': str(deck_tuple[4]),
            'rating': float(deck_tuple[5]),
            'created_at': deck_tuple[6].isoformat() if deck_tuple[6] else None,
            'updated_at': deck_tuple[7].isoformat() if deck_tuple[7] else None,
            'owner': deck_tuple[8],
            'card_count': int(deck_tuple[9])
        }
    else:
        # Fallback pour des formats non reconnus
        return deck_tuple


def serialize_deck_data(deck_data):
    """
    Sérialise les données de deck(s) en format JSON avec les champs comme clés.
    Peut accepter un seul deck ou une liste de decks.
    """
    if isinstance(deck_data, DeckModel):
        # Si c'est une instance de DeckModel
        return {
            'id': str(deck_data.id),
            'name': deck_data.name,
            'description': deck_data.description,
            'publish_status': deck_data.publish_status,
            'owner_id': str(deck_data.owner_id),
            'rating': float(deck_data.rating),
            'created_at': deck_data.created_at.isoformat() if deck_data.created_at else None,
            'updated_at': deck_data.updated_at.isoformat() if deck_data.updated_at else None,
        }
    elif isinstance(deck_data, (list, tuple)) and deck_data:
        if isinstance(deck_data[0], (list, tuple)):
            # Liste de tuples (résultats de requêtes SQL)
            return [serialize_single_deck_tuple(deck) for deck in deck_data]
        else:
            # Tuple unique (résultat d'une requête SQL)
            return serialize_single_deck_tuple(deck_data)
    else:
        return deck_data
