import uuid

import bcrypt
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.request import Request
from pyramid.view import view_config


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

    with db_conn.cursor() as cur:
        # Check if email or username already exists, if it does send error
        cur.execute(
            "SELECT * FROM users WHERE email = %s OR username = %s",
            (email, username))
        record = cur.fetchone()

        if record is not None:
            request.response.status = 400
            return {"error": "Email or username already taken"}

        # Hash the password
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        # Generate UUID for the new user
        user_id = str(uuid.uuid4())

        # Add new user to DB
        cur.execute(
            """
            INSERT INTO users (id, first_name, last_name, username, email, password_hash) 
               VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, first_name, last_name, username, email, hashed_password.decode('utf-8'))
        )

        # Generate user details id
        details_id = str(uuid.uuid4())

        # Generate empty user details row
        cur.execute(
            """
            INSERT INTO user_details (id, user_id, about_me)
                VALUES (%s, %s, %s)
            """,
            (details_id, user_id, "")
        )

        db_conn.commit()

    return {
        'message': 'User registered successfully',
        'user': {
            'firstName': first_name,
            'lastName': last_name,
            'username': username,
            'email': email
        },
        'token': user_id,
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

    with db_conn.cursor() as cur:
        # Check if user exists
        cur.execute(
            "SELECT id, first_name, last_name, username, email, password_hash FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()

        if user is None:
            request.response.status = 400
            return {"error": "Invalid credentials"}

        # Compare passwords
        stored_hash = user[5].encode('utf-8')
        is_same = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        
        if not is_same:
            request.response.status = 400
            return {"error": "Invalid credentials"}

        return {
            'message': 'Login successful',
            'user': {
                'id': user[0],
                'firstName': user[1],
                'lastName': user[2],
                'username': user[3],
                'email': user[4]
            },
            'token': user[0],
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
