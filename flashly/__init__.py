import os

from dotenv import load_dotenv
from pyramid.config import Configurator


def main(global_config, **settings):
    # load enviroment variables
    load_dotenv()

    # update settings object with enviroment variables
    env_vars = {
        'db.host': os.getenv('DB_HOST', 'localhost'),
        'db.name': os.getenv('DB_NAME', 'flashly'),
        'db.user': os.getenv('DB_USER'),
        'db.password': os.getenv('DB_PASSWORD'),
        'db.port': os.getenv('DB_PORT', '5432'),
        'secret_key': os.getenv('SECRET_KEY'),
    }
    settings.update(env_vars)
    
    config = Configurator(settings=settings)
    config.include('.routes')
    config.include('.models')
    config.scan()

    return config.make_wsgi_app()
