import webbrowser
import argparse
import os

from timevis import app


def parse_args():
    parser = argparse.ArgumentParser(description='TimeVis')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='Enable browser')

    config_default = os.path.join(os.getcwd(), 'config.py')
    parser.add_argument('-c', '--config', default=config_default,
                        help='Configuration file')

    parser.add_argument('-p', '--port', default=8000, help='Port')
    parser.add_argument('-s', '--host', default='0.0.0.0', help='Host')
    parser.add_argument('-d', '--debug', default=False, help='Debug mode')

    return parser.parse_args()


def main(port=8000):
    # Parse args
    args = parse_args()

    # Load customize config files
    if os.path.exists(args.config):
        app.config.from_pyfile(args.config)

    # Open a window
    if args.browser:
        webbrowser.open("http://localhost:{}".format(port))

    # Begin the server
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
