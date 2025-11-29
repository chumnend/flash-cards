from pyramid.request import Request
from pyramid.view import view_config


@view_config(
    route_name="get_profile",
    request_method="GET",
    renderer="json"
)
def get_profile(request: Request):
    user_id = request.matchdict['user_id']

    # Fetch database connector
    db_conn = request.db_conn

    with db_conn.cursor() as cur:
        # Find the user in database
        cur.execute(
            """
            SELECT id, first_name, last_name, username, email, created_at, updated_at
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )
        user = cur.fetchone()
        if not user:
            request.response.status_code = 404
            return {
                'error': 'User not found',
            }

        # Fetch user details
        cur.execute(
            """
            SELECT about_me
            FROM user_details
            WHERE user_id = %s
            """,
            (user_id,)
        )
        user_details = cur.fetchone()

        # Fetch following
        cur.execute(
            """
            SELECT COUNT(*) as following_count
            FROM followers 
            WHERE follower_id = %s
            """,
            (user_id,)
        )
        following_count = cur.fetchone()[0]

        # Fetch followers
        cur.execute(
            """
            SELECT COUNT(*) as followers_count
            FROM followers 
            WHERE following_id = %s
            """,
            (user_id,)
        )
        followers_count = cur.fetchone()[0]

        # Fetch decks
        cur.execute(
            """
            SELECT id, name, description, publish_status, rating, created_at, updated_at
            FROM decks 
            WHERE owner_id = %s
            """, 
            (user_id,)
        )
        decks = cur.fetchall()

        # Build decks with cards and categories
        decks_with_details = []
        for deck in decks:
            deck_id = deck[0]
            
            # Fetch cards for this deck
            cur.execute(
                """
                SELECT id, front_text, back_text, difficulty, times_reviewed, success_rate, created_at, updated_at
                FROM cards
                WHERE deck_id = %s
                """,
                (deck_id,)
            )
            cards = cur.fetchall()
            
            # Fetch categories for this deck
            cur.execute(
                """
                SELECT c.id, c.name, c.created_at, c.updated_at
                FROM categories c
                JOIN deck_categories dc ON c.id = dc.category_id
                WHERE dc.deck_id = %s
                """,
                (deck_id,)
            )
            categories = cur.fetchall()
            
            deck_obj = {
                'id': deck[0],
                'name': deck[1],
                'description': deck[2],
                'publish_status': deck[3],
                'rating': float(deck[4]) if deck[4] else 0.0,
                'created_at': deck[5].isoformat() if deck[5] else None,
                'updated_at': deck[6].isoformat() if deck[6] else None,
                'cards': [
                    {
                        'id': card[0],
                        'front_text': card[1],
                        'back_text': card[2],
                        'difficulty': card[3],
                        'times_reviewed': card[4],
                        'success_rate': float(card[5]) if card[5] else 0.0,
                        'created_at': card[6].isoformat() if card[6] else None,
                        'updated_at': card[7].isoformat() if card[7] else None
                    }
                    for card in cards
                ],
                'categories': [
                    {
                        'id': category[0],
                        'name': category[1],
                        'created_at': category[2].isoformat() if category[2] else None,
                        'updated_at': category[3].isoformat() if category[3] else None
                    }
                    for category in categories
                ]
            }
            decks_with_details.append(deck_obj)

    # build complete user profile
    profile = {
        'id': user[0],
        'first_name': user[1],
        'last_name': user[2],
        'username': user[3],
        'email': user[4],
        'created_at': user[5].isoformat() if user[5] else None,
        'updated_at': user[6].isoformat() if user[6] else None,
        'about_me': user_details[0] if user_details else None,
        'following_count': following_count,
        'followers_count': followers_count,
        'decks': decks_with_details
    }

    return {
        'message': f'/users/{user_id} route hit',
        'profile': profile,
    }


@view_config(
    route_name="update_user",
    request_method="PUT",
    renderer="json"
)
def update_user(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id} update route hit'
    }


@view_config(
    route_name="change_password",
    request_method="PUT",
    renderer="json"
)
def change_password(request: Request):
    return {
        'message': '/change_password route hit'
    }


@view_config(
    route_name="follow",
    request_method="POST",
    renderer="json"
)
def follow(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id}/follow route hit'
    }


@view_config(
    route_name="unfollow",
    request_method="DELETE",
    renderer="json"
)
def unfollow(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id}/unfollow route hit'
    }


@view_config(
    route_name="get_followers",
    request_method="GET",
    renderer="json"
)
def get_followers(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id}/followers route hit'
    }


@view_config(
    route_name="get_following",
    request_method="GET",
    renderer="json"
)
def get_following(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id}/following route hit'
    }
