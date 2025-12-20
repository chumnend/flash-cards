import uuid
from datetime import datetime

from pyramid.request import Request
from pyramid.view import view_config

from flashly.models import DeckModel
from flashly.utils.serialize import serialize_deck_data


@view_config(
    route_name="explore_decks",
    request_method="GET",
    renderer="json"
)
def explore_decks(request: Request):
    # Fetch database connector
    db_conn = request.db_conn

    # Fetch explore feed
    decks = DeckModel.find_explore_decks(db_conn)
    if decks is None:
        request.response.status_code = 500
        return {
            'error': 'Unable to load explore feed',
        }

    return {
        'message': 'Explore feed loaded successfully',
        'decks': serialize_deck_data(decks),
    }


@view_config(
    route_name="feed",
    request_method="GET",
    renderer="json"
)
def feed(request: Request):
    # Fetch database connector
    db_conn = request.db_conn

    # Get token from request
    token = request.params.get('token')

    # Fetch feed of user
    decks = DeckModel.find_feed_decks(db_conn, token)
    if decks is None:
        request.response.status_code = 500
        return {
            'error': 'Unable to load user feed',
        }

    return {
        'message': 'User feed loaded successfully',
        'decks': serialize_deck_data(decks),
    }


@view_config(
    route_name="get_decks",
    request_method="GET",
    renderer="json"
)
def get_decks(request: Request):
    # Fetch database connector
    db_conn = request.db_conn

    # Get token from request
    token = request.params.get('token')

    # Fetch user's decks
    decks = DeckModel.find_decks_by_user_id(db_conn, token)
    if decks is None:
        request.response.status_code = 500
        return {
            'error': "Unable to load user's decks",
        }

    return {
        'message': 'User feed loaded successfully',
        'decks': serialize_deck_data(decks),
    }


@view_config(
    route_name="create_deck",
    request_method="POST",
    renderer="json"
)
def create_deck(request: Request):
    # Get JSON request
    try:
        data = request.json_body
    except (ValueError, UnicodeDecodeError):
        request.response.status = 400
        return {"error": "Invalid JSON"}
    
    # Validate that all required fields are present
    required_fields = ["name", "description"]
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        request.response.status = 400
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}
    
    # Extract data
    name = data['name'].strip()
    description = data.get('description', '').strip()
    publish_status = data.get('publishStatus', 'private').strip()

    # Get token from request
    token = request.params.get('token')

    # Fetch database connector
    db_conn = request.db_conn

    # Create new deck
    new_deck = DeckModel(
        id=str(uuid.uuid4()),
        name=name,
        description=description,
        publish_status=publish_status,
        owner_id=token,
        rating=0.0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    new_deck.save(db_conn)

    return {
        'message': 'Deck successfully created',
        'deck': serialize_deck_data(new_deck),
    }


@view_config(
    route_name="get_deck",
    request_method="GET",
    renderer="json"
)
def get_deck(request: Request):
    deck_id = request.matchdict['deck_id']

    # Fetch database connector
    db_conn = request.db_conn

    # Find deck
    deck = DeckModel.find_deck_by_id(db_conn, deck_id)
    if deck is None:
        request.response.status_code = 500
        return {
            'error': "Unable to load deck",
        }  
    
    return {
        'message': 'Deck loaded successfully',
        'deck': serialize_deck_data(deck),
    }


@view_config(
    route_name="update_deck",
    request_method="PUT",
    renderer="json"
)
def update_deck(request: Request):
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

    # Find the existing deck
    existing_deck_data = DeckModel.find_deck_by_id(db_conn, deck_id)
    if existing_deck_data is None:
        request.response.status_code = 404
        return {"error": "Deck not found"}

    # Check if the user owns this deck
    if str(existing_deck_data[4]) != token:  # owner_id is at index 4
        request.response.status_code = 403
        return {"error": "You can only update your own decks"}   

    # Extract and validate data
    name = data.get('name', existing_deck_data[1]).strip()  # name is at index 1
    description = data.get('description', existing_deck_data[2]).strip()  # description is at index 2
    publish_status = data.get('publishStatus', existing_deck_data[3]).strip()  # publish_status is at index 3

    # Validate required fields
    if not name:
        request.response.status_code = 400
        return {"error": "Name cannot be empty"}
    
    # Validate publish_status
    valid_statuses = ['private', 'public']
    if publish_status not in valid_statuses:
        request.response.status_code = 400
        return {"error": f"Invalid publish status. Must be one of: {', '.join(valid_statuses)}"}

    # Create updated deck model
    updated_deck = DeckModel(
        id=existing_deck_data[0],  # id
        name=name,
        description=description,
        publish_status=publish_status,
        owner_id=existing_deck_data[4],  # owner_id
        rating=existing_deck_data[5],  # rating
        created_at=existing_deck_data[6],  # created_at
        updated_at=datetime.now()
    )
    
    # Save the updated deck
    updated_deck.update(db_conn)

    # Fetch the updated deck to return complete data
    updated_deck_data = DeckModel.find_deck_by_id(db_conn, deck_id)

    return {
        'message': 'Deck updated successfully',
        'deck': serialize_deck_data(updated_deck_data),
    }

@view_config(
    route_name="delete_deck",
    request_method="DELETE",
    renderer="json"
)
def delete_deck(request: Request):
    deck_id = request.matchdict['deck_id']
    
    # Get token from request
    token = request.params.get('token')
    if not token:
        request.response.status_code = 400
        return {"error": "Token is required"}
    
    # Fetch database connector
    db_conn = request.db_conn
    
    # Find the existing deck
    existing_deck_data = DeckModel.find_deck_by_id(db_conn, deck_id)
    if existing_deck_data is None:
        request.response.status_code = 404
        return {"error": "Deck not found"}
    
    # Check if the user owns this deck
    if str(existing_deck_data[4]) != token:  # owner_id is at index 4
        request.response.status_code = 403
        return {"error": "You can only delete your own decks"}

    try:
        # Create DeckModel instance for deletion
        deck_to_delete = DeckModel(
            id=existing_deck_data[0],  # id
            name=existing_deck_data[1],  # name
            description=existing_deck_data[2],  # description
            publish_status=existing_deck_data[3],  # publish_status
            owner_id=existing_deck_data[4],  # owner_id
            rating=existing_deck_data[5],  # rating
            created_at=existing_deck_data[6],  # created_at
            updated_at=existing_deck_data[7]   # updated_at
        )
        
        # Delete the deck (cards and categories will be deleted automatically due to CASCADE)
        deck_to_delete.delete(db_conn)
        
        return {
            'message': 'Deck successfully deleted'
        }
        
    except Exception as e:
        print(f"Error deleting deck: {e}")
        request.response.status_code = 500
        return {"error": "Failed to delete deck"}
