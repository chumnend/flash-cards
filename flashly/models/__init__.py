from psycopg2.pool import SimpleConnectionPool

from .user import UserModel
from .user_details import UserDetailsModel
from .deck import DeckModel

def includeme(config):
    """
    Initiailize the modal for the Pyramid App
    """
    settings = config.get_settings()

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

    config.registry.settings['db_pool'] = db_pool

    def get_db_connection(request):
        pool = request.registry.settings['db_pool']
        conn = pool.getconn()

        def cleanup(request):
            pool.putconn(conn)
        
        request.add_finished_callback(cleanup)
        return conn

    config.add_request_method(get_db_connection, 'db_conn', reify=True)
