from pyramid.request import Request
from pyramid.view import view_config


@view_config(
    route_name="get_cards",
    request_method="GET",
    renderer="json"
)
def get_cards(request: Request):
    deck_id = request.matchdict['deck_id']
    return {
        'message': f'/decks/{deck_id}/cards route hit'
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
