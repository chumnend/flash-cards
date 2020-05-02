from flask import Blueprint, render_template
errors = Blueprint('errors', __name__)

# PAGE NOT FOUND ====================================================
@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

# SERVER ERROR ======================================================
@errors.app_errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
