from pyramid.request import Request
from pyramid.view import view_config


@view_config(
    route_name="get_profile",
    request_method="GET",
    renderer="json"
)
def get_profile(request: Request):
    user_id = request.matchdict['user_id']
    return {
        'message': f'/users/{user_id} route hit'
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
