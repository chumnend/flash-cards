import uuid
from datetime import datetime

from pyramid.request import Request
from pyramid.view import view_config

from flashly.models import UserModel
from flashly.models import UserDetailsModel

@view_config(
    route_name="register",
    request_method="POST",
    renderer='json',
)
def register(request: Request):
    # Get JSON request
    try:
        data = request.json_body
    except (ValueError, UnicodeDecodeError):
        request.response.status = 400
        return {"error": "Invalid JSON"}

    # Validate that all required fields are present
    required_fields = ["firstName", "lastName", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        request.response.status = 400
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

    # Validate the email has the correct format
    email = data['email'].strip().lower()
    if '@' not in email or '.' not in email:
        request.response.status = 400
        return {"error": "Invalid email format"}

    # Validate the password has the correct format
    password = data['password']
    if len(password) < 6:
        request.response.status = 400
        return {"error": "Password must be at least 6 characters long"}
    
    first_name = data['firstName'].strip().title()
    last_name = data['lastName'].strip().title()
    username = data['username'].strip().title()

    # Fetch database connector
    db_conn = request.db_conn

    # Check if email or username already exists
    existing_user_email = UserModel.find_by_email(db_conn, email)
    existing_user_username = UserModel.find_by_username(db_conn, username)
    if existing_user_email or existing_user_username:
        request.response.status = 400
        return {"error": "Email or username already taken"}

    # Create new user
    user = UserModel(
        id=uuid.uuid4(),
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password_hash="",  # Will be set by set_password
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    user.set_password(password) # Set password (this will hash it)

    # Create new user details
    user_details = UserDetailsModel(
        id=uuid.uuid4(),
        user_id=user.id,
        about_me="",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Save user to database
    user.save(db_conn)
    user_details.save(db_conn)

    return {
        'message': 'User registered successfully',
        'user': {
            'id': str(user.id),
            'firstName': user.first_name,
            'lastName': user.last_name,
            'username': user.username,
            'email': user.email
        },
        'token': str(user.id),
    }


@view_config(
    route_name="login",
    request_method="POST",
    renderer="json"
)
def login(request: Request):
    # Get JSON request
    try:
        data = request.json_body
    except (ValueError, UnicodeDecodeError):
        request.response.status = 400
        return {"error": "Invalid JSON"}

    # Validate that all required fields are present
    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        request.response.status = 400
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}

    # Fetch email and validate that is looks correct, if it has wrong format no need to hit DB
    email = data['email'].strip().lower()
    if '@' not in email or '.' not in email:
        request.response.status = 400
        return {"error": "Invalid credentials"}
    
    # Fetch password and validate that is looks correct, if it has wrong format no need to hit DB
    password = data['password']
    if len(password) < 6:
        request.response.status = 400
        return {"error": "Invalid credentials"}
    
    # Fetch database connector
    db_conn = request.db_conn

    # Find user by email using the model
    user = UserModel.find_by_email(db_conn, email)
    if user is None:
        request.response.status = 400
        return {"error": "Invalid credentials"}
    
    # Check password using the model method
    if not user.check_password(password):
        request.response.status = 400
        return {"error": "Invalid credentials"}

    return {
        'message': 'Login successful',
        'user': {
            'id': str(user.id),
            'firstName': user.first_name,
            'lastName': user.last_name,
            'username': user.username,
            'email': user.email
        },
        'token': str(user.id),
    }


@view_config(
    route_name="logout",
    request_method="POST",
    renderer="json"
)
def logout(request: Request):
    return {
        'message': '/logout route hit'
    }

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
        # Single comprehensive query to get all user profile data
        cur.execute(
            """
            SELECT 
                u.id, u.first_name, u.last_name, u.username, u.email, u.created_at, u.updated_at,
                ud.about_me,
                COALESCE(following.following_count, 0) as following_count,
                COALESCE(followers.followers_count, 0) as followers_count,
                d.id as deck_id, d.name as deck_name, d.description as deck_description, 
                d.publish_status, d.rating as deck_rating, d.created_at as deck_created_at, 
                d.updated_at as deck_updated_at,
                c.id as card_id, c.front_text, c.back_text, c.difficulty, c.times_reviewed, 
                c.success_rate as card_success_rate, c.created_at as card_created_at, 
                c.updated_at as card_updated_at,
                cat.id as category_id, cat.name as category_name, 
                cat.created_at as category_created_at, cat.updated_at as category_updated_at
            FROM users u
            LEFT JOIN user_details ud ON u.id = ud.user_id
            LEFT JOIN (
                SELECT follower_id, COUNT(*) as following_count 
                FROM followers 
                GROUP BY follower_id
            ) following ON u.id = following.follower_id
            LEFT JOIN (
                SELECT following_id, COUNT(*) as followers_count 
                FROM followers 
                GROUP BY following_id
            ) followers ON u.id = followers.following_id
            LEFT JOIN decks d ON u.id = d.owner_id
            LEFT JOIN cards c ON d.id = c.deck_id
            LEFT JOIN deck_categories dc ON d.id = dc.deck_id
            LEFT JOIN categories cat ON dc.category_id = cat.id
            WHERE u.id = %s
            ORDER BY d.id, c.id, cat.id
            """,
            (user_id,)
        )
        
        results = cur.fetchall()
        
        if not results or not results[0][0]:  # Check if user exists
            request.response.status_code = 404
            return {
                'error': 'User not found',
            }

        # Process the results to build the profile structure
        user_data = results[0]
        profile = {
            'id': user_data[0],
            'first_name': user_data[1],
            'last_name': user_data[2],
            'username': user_data[3],
            'email': user_data[4],
            'created_at': user_data[5].isoformat() if user_data[5] else None,
            'updated_at': user_data[6].isoformat() if user_data[6] else None,
            'about_me': user_data[7],
            'following_count': user_data[8],
            'followers_count': user_data[9],
            'decks': []
        }

        # Group results by deck
        decks_dict = {}
        for row in results:
            deck_id = row[10]  # deck_id
            if deck_id and deck_id not in decks_dict:
                decks_dict[deck_id] = {
                    'id': deck_id,
                    'name': row[11],  # deck_name
                    'description': row[12],  # deck_description
                    'publish_status': row[13],
                    'rating': float(row[14]) if row[14] else 0.0,
                    'created_at': row[15].isoformat() if row[15] else None,
                    'updated_at': row[16].isoformat() if row[16] else None,
                    'cards': {},
                    'categories': {}
                }

            if deck_id:
                # Add cards
                card_id = row[17]  # card_id
                if card_id and card_id not in decks_dict[deck_id]['cards']:
                    decks_dict[deck_id]['cards'][card_id] = {
                        'id': card_id,
                        'front_text': row[18],
                        'back_text': row[19],
                        'difficulty': row[20],
                        'times_reviewed': row[21],
                        'success_rate': float(row[22]) if row[22] else 0.0,
                        'created_at': row[23].isoformat() if row[23] else None,
                        'updated_at': row[24].isoformat() if row[24] else None
                    }

                # Add categories
                category_id = row[25]  # category_id
                if category_id and category_id not in decks_dict[deck_id]['categories']:
                    decks_dict[deck_id]['categories'][category_id] = {
                        'id': category_id,
                        'name': row[26],
                        'created_at': row[27].isoformat() if row[27] else None,
                        'updated_at': row[28].isoformat() if row[28] else None
                    }

        # Convert dictionaries to lists
        for deck in decks_dict.values():
            deck['cards'] = list(deck['cards'].values())
            deck['categories'] = list(deck['categories'].values())

        profile['decks'] = list(decks_dict.values())

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
