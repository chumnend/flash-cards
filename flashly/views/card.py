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
    
    # Get JSON request
    try:
        data = request.json_body
    except (ValueError, UnicodeDecodeError):
        request.response.status_code = 400
        return {"error": "Invalid JSON"}
    
    # Get token from request
    token = request.params.get('token')
    if not token:
        request.response.status_code = 400
        return {"error": "Token is required"}
    
    # Fetch database connector
    db_conn = request.db_conn
    
    # Verify that the deck exists
    deck = DeckModel.find_deck_by_id(db_conn, deck_id)
    if deck is None:
        request.response.status_code = 404
        return {"error": "Deck not found"}
    
    # Check if the user owns this deck
    deck_owner_id = deck[4]  # owner_id is at index 4
    if str(deck_owner_id) != token:
        request.response.status_code = 403
        return {"error": "You can only add cards to your own decks"}
    
    # Validate that all required fields are present
    required_fields = ["frontText", "backText"]
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        request.response.status_code = 400
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}
    
    # Extract data
    front_text = data['frontText'].strip()
    back_text = data['backText'].strip()
    difficulty = data.get('difficulty', 'easy').strip()
    
    # Validate difficulty
    valid_difficulties = ['easy', 'medium', 'hard']
    if difficulty not in valid_difficulties:
        request.response.status_code = 400
        return {"error": f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}"}
    
    try:
        # Create new card
        new_card = CardModel(
            id=str(uuid.uuid4()),
            front_text=front_text,
            back_text=back_text,
            difficulty=difficulty,
            times_reviewed=0,
            success_rate=0.0,
            deck_id=deck_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        new_card.save(db_conn)
        
        # Update the deck's updated_at timestamp
        # First get the deck as a DeckModel instance
        updated_deck = DeckModel(
            id=deck[0],
            name=deck[1],
            description=deck[2],
            publish_status=deck[3],
            owner_id=deck[4],
            rating=deck[5],
            created_at=deck[6],
            updated_at=datetime.now()
        )
        updated_deck.update(db_conn)
        
        return {
            'message': 'Card successfully created',
            'card': serialize_card_data(new_card),
        }
        
    except Exception as e:
        print(f"Error creating card: {e}")
        request.response.status_code = 500
        return {"error": "Failed to create card"}


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
