from pyramid.request import Request
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest


@view_config(
    route_name="register",
    request_method="POST",
    renderer='json',
)
def register(request: Request):
    try:
        data = request.json_body
    except (ValueError, UnicodeDecodeError):
        raise HTTPBadRequest("Invalid JSON")
    
    # Validate that all required fields are present
    required_fields = ["firstName", "lastName", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing_fields:
        return {
            'error': f"Missing required fields: {', '.join(missing_fields)}",
            'status': 'error'
        }
    
    # Valdiate the email has the correct format
    email = data['email'].strip().lower()
    if '@' not in email or '.' not in email:
        return {
            'error': 'Invalid email format',
            'status': 'error'
        }
    
    # Validate the password has the correct format
    password = data['password']
    if len(password) < 6:
        return {
            'error': 'Password must be at least 6 characters long',
            'status': 'error'
        }
    
    firstname = data['firstName'].strip().title()
    lastname = data['lastName'].strip().title()

    db_conn = request.db_conn

    # TODO: Verify email does not already exists
    # TODO: hash the password
    # TODO: Add new user to DB

    return {
        'message': 'User registered successfully',
        'user': {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        },
        'status': 'success'
    }


@view_config(
    route_name="login",
    request_method="POST",
    renderer="json"
)
def login(request: Request):
    return {
        'message': '/login route hit'
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
    route_name="change_password",
    request_method="PUT",
    renderer="json"
)
def change_password(request: Request):
    return {
        'message': '/change_password route hit'
    }
