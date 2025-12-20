import uuid
from datetime import datetime

from pyramid.request import Request
from pyramid.view import view_config

from flashly.models.deck import DeckModel
from flashly.models.card import CardModel, serialize_card_data

@view_config(
    route_name="get_cards",
    request_method="GET",
    renderer="json"
)
def get_cards(request: Request):
    deck_id = request.matchdict['deck_id']
    
    # Fetch database connector
    db_conn = request.db_conn
    
    # Verify that the deck exists
    deck = DeckModel.find_deck_by_id(db_conn, deck_id)
    if deck is None:
        request.response.status_code = 404
        return {
            'error': 'Deck not found',
        }
    
    # Get token from request (optional for public decks)
    token = request.params.get('token')
    
    # Check if deck is private and user has access
    deck_publish_status = deck[3]  # publish_status is at index 3
    deck_owner_id = deck[4]        # owner_id is at index 4
    
    if deck_publish_status == 'private':
        if not token or str(deck_owner_id) != token:
            request.response.status_code = 403
            return {
                'error': 'Access denied. This is a private deck.',
            }
    
    # Fetch cards for this deck
    cards = CardModel.find_cards_by_deck_id(db_conn, deck_id)
    if cards is None:
        request.response.status_code = 500
        return {
            'error': 'Unable to load cards',
        }
    
    return {
        'message': f'Cards for deck {deck_id} loaded successfully',
        'cards': serialize_card_data(cards),
        'deck_info': {
            'id': str(deck[0]),
            'name': deck[1],
            'card_count': len(cards)
        }
    }


@view_config(
    route_name="create_card",
    request_method="POST",
    renderer="json"
)
def create_card(request: Request):
    deck_id = request.matchdict['deck_id']
    return {
        'message': f'/decks/{deck_id}/cards create route hit'
    }


@view_config(
    route_name="get_card",
    request_method="GET",
    renderer="json"
)
def get_card(request: Request):
    deck_id = request.matchdict['deck_id']
    card_id = request.matchdict['card_id']
    return {
        'message': f'/decks/{deck_id}/cards/{card_id} route hit'
    }


@view_config(
    route_name="update_card",
    request_method="PUT",
    renderer="json"
)
def update_card(request: Request):
    deck_id = request.matchdict['deck_id']
    card_id = request.matchdict['card_id']
    return {
        'message': f'/decks/{deck_id}/cards/{card_id} update route hit'
    }


@view_config(
    route_name="delete_card",
    request_method="DELETE",
    renderer="json"
)
def delete_card(request: Request):
    deck_id = request.matchdict['deck_id']
    card_id = request.matchdict['card_id']
    return {
        'message': f'/decks/{deck_id}/cards/{card_id} delete route hit'
    }
