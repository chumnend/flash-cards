import os

from pyramid.request import Request
from pyramid.view import view_config
from pyramid.response import FileResponse


@view_config(
    route_name="frontend",
    request_method="GET",
)
def spa_view(request: Request):
    """Serve the main SPA HTML file for all non-API routes"""
    here = os.path.dirname(__file__)
    # Go up two levels from views/ to get to the package root
    dist_path = os.path.join(here, '..', 'dist', 'index.html')
    return FileResponse(dist_path)


@view_config(
    route_name="frontend_catchall",
    request_method="GET",
)
def spa_catchall(request: Request):
    """Serve the main SPA HTML file for all non-API, non-static routes"""
    # Don't serve HTML for static file requests
    path = request.subpath
    if path and len(path) > 0:
        # Check if this looks like a static file request
        last_segment = path[-1] if path else ""
        if any(last_segment.endswith(ext) for ext in ['.js', '.css', '.png', '.jpg', '.ico', '.svg', '.woff', '.woff2']):
            # Let this fall through - it should be handled by static view or return 404
            from pyramid.httpexceptions import HTTPNotFound
            raise HTTPNotFound()
    
    here = os.path.dirname(__file__)
    dist_path = os.path.join(here, '..', 'dist', 'index.html')
    return FileResponse(dist_path)