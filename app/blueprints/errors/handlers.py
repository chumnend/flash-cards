from flask import render_template
from app.blueprints.errors import bp

# PAGE NOT FOUND ====================================================
@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

# SERVER ERROR ======================================================
@bp.app_errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
