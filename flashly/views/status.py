from pyramid.request import Request
from pyramid.view import view_config
import datetime


@view_config(
    route_name="status",
    request_method="GET",
    renderer="json",
)
def status_check(request: Request):
    return {
        "status": "running",
        "message": "Backend is healthy",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
