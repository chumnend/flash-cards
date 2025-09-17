from pyramid.request import Request
from pyramid.view import view_config

@view_config(
        route_name="hello",
        request_method="GET",
        renderer='json',
)
def hello_world(request: Request):
    """
    Returns a message. 

    :param request: a pyramid request object
    """
    return {
        'message': 'Hello World!',
    }
