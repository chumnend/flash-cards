import os

from dotenv import load_dotenv
from pyramid.config import Configurator
from psycopg2.pool import SimpleConnectionPool


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
    
    # create db pool for psql
    db_pool = SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        host=settings.get('db.host', 'localhost'),
        database=settings.get('db.name', 'flashly_dev'),
        user=settings.get('db.user', 'user'),
        password=settings.get('db.password', 'password'),
        port=settings.get('db.port', 5432),
    )

    def get_db_connection(request):
        pool = request.registry.settings['db_pool']
        conn = pool.getconn()

        def cleanup(request):
            pool.putconn(conn)
        
        request.add_finished_callback(cleanup)
        return conn
    
    config = Configurator(settings=settings)
    config.registry.settings['db_pool'] = db_pool
    config.add_request_method(get_db_connection, 'db_conn', reify=True)
    config.include('.routes')
    config.scan()

    return config.make_wsgi_app()
