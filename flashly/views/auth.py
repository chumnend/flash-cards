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
            'firstName': first_name,
            'lastName': last_name,
            'username': username,
            'email': email
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
