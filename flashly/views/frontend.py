import os

from pyramid.response import FileResponse, Response
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='frontend')
def frontend_view(request: Request):
    """Serve the React SPA for all non-API routes"""
    # Path to your built React app's index.html
    package_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(package_dir, 'dist')
    index_path = os.path.join(static_dir, 'index.html')
    
    if os.path.exists(index_path):
        return FileResponse(index_path, content_type='text/html')
    else:
        # Fallback if build doesn't exist
        return Response(
            body="React app not built. Run 'yarn run build' in frontend directory.",
            status=404,
            content_type='text/plain'
        )