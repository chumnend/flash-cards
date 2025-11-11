from pyramid.request import Request
from pyramid.view import view_config


@view_config(
    route_name="explore_decks",
    request_method="GET",
    renderer="json"
)
def explore_decks(request: Request):
    return {
        'message': '/decks/explore route hit'
    }


@view_config(
    route_name="feed",
    request_method="GET",
    renderer="json"
)
def feed(request: Request):
    return {
        'message': '/decks/feed route hit'
    }


@view_config(
    route_name="get_decks",
    request_method="GET",
    renderer="json"
)
def get_decks(request: Request):
    return {
        'message': '/decks route hit'
    }


@view_config(
    route_name="create_deck",
    request_method="POST",
    renderer="json"
)
def create_deck(request: Request):
    return {
        'message': '/decks create route hit'
    }


@view_config(
    route_name="get_deck",
    request_method="GET",
    renderer="json"
)
def get_deck(request: Request):
    deck_id = request.matchdict['deck_id']
    return {
        'message': f'/decks/{deck_id} route hit'
    }


@view_config(
    route_name="update_deck",
    request_method="PUT",
    renderer="json"
)
def update_deck(request: Request):
    deck_id = request.matchdict['deck_id']
    return {
        'message': f'/decks/{deck_id} update route hit'
    }


@view_config(
    route_name="delete_deck",
    request_method="DELETE",
    renderer="json"
)
def delete_deck(request: Request):
    deck_id = request.matchdict['deck_id']
    return {
        'message': f'/decks/{deck_id} delete route hit'
    }
