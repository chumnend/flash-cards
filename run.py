import argparse
from waitress import serve

from flashly import main

def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=6543)
    parser.add_argument('--reload', action='store_true')

    args = parser.parse_args()

    settings = {
        'pyramid.reload_templates': args.reload,
        'pyramid.debug_authorization': args.reload,
    }

    app = main({}, **settings)
    print(f'Server started on http://{args.host}:{args.port}')
    serve(app, host=args.host, port=args.port)

if __name__ == '__main__':
    run_server()
