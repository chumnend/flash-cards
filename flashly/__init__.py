import os

from dotenv import load_dotenv
from pyramid.config import Configurator


def main(global_config=None, **settings):
    """
    This function creates and configures a Pyramid WSGI application

    :param global_config: unused in this application
    :param settings: Configuration key/value pairs
    :returns: a Pyramid WSGI application
    """

    # load enviroment variables
    load_dotenv()

    # update settings object with enviroment variables
    env_vars = {
        "db.host": os.getenv("DB_HOST", "localhost"),
        "db.name": os.getenv("DB_NAME", "flashly"),
        "db.user": os.getenv("DB_USER"),
        "db.password": os.getenv("DB_PASSWORD"),
        "db.port": os.getenv("DB_PORT", "5432"),
        "secret_key": os.getenv("SECRET_KEY"),
    }
    settings.update(env_vars)

    with Configurator(settings=settings) as config:
        # Add static views for React build files
        config.add_static_view('static', 'flashly:client/dist', cache_max_age=3600)
        config.add_static_view('assets', 'flashly:client/dist/assets', cache_max_age=31536000)  # 1 year cache for assets
        
        config.include(".routes")
        config.include(".models")
        config.scan()

    return config.make_wsgi_app()
