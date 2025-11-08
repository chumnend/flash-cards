def includeme(config):
    config.add_route('hello', '/')

    # Authentication Routes
    config.add_route('register', '/register', request_method='POST')
    config.add_route('login', '/login', request_method='POST')
    config.add_route('logout', '/logout', request_method='POST')
    config.add_route('change_password', '/change_password', request_method='PUT')

    # User Routes
    config.add_route('get_profile', '/users/{user_id}', request_method='GET')
    config.add_route('update_user', '/users/{user_id}', request_method='PUT')
    config.add_route('follow', '/users/{user_id}/follow', request_method='POST')
    config.add_route('unfollow', '/users/{user_id}/unfollow', request_method='DELETE')
    config.add_route('get_followers', '/users/{user_id}/followers', request_method='GET')
    config.add_route('get_following', '/users/{user_id}/following', request_method='GET')

    # Deck Routes
    config.add_route('explore_decks', '/decks/explore', request_method='GET')
    config.add_route('feed', '/decks/feed', request_method='GET')
    config.add_route('get_decks', '/decks', request_method='GET')
    config.add_route('create_deck', '/decks', request_method='POST')
    config.add_route('get_deck', '/decks/{deck_id}', request_method='GET')
    config.add_route('update_deck', '/decks/{deck_id}', request_method='PUT')
    config.add_route('delete_deck', '/decks/{deck_id}', request_method='DELETE')

    # Card Routes
    config.add_route('get_cards', '/decks/{deck_id}/cards', request_method='GET')
    config.add_route('create_card', '/decks/{deck_id}/cards', request_method='POST')
    config.add_route('get_card', '/decks/{deck_id}/cards/{card_id}', request_method='GET')
    config.add_route('update_card', '/decks/{deck_id}/cards/{card_id}', request_method='PUT')
    config.add_route('delete_card', '/decks/{deck_id}/cards/{card_id}', request_method='DELETE')
