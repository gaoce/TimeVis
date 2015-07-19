#!/usr/bin/env python
import webbrowser
import argparse
from . import app


def parse_args():
    parser = argparse.ArgumentParser(description='TimeVis')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='Enable browser')
    parser.add_argument('-p', '--port', default=8000, help='Port')
    parser.add_argument('-s', '--host', default='0.0.0.0', help='Host')
    parser.add_argument('-d', '--debug', default=False, help='Debug mode')

    return parser.parse_args()


def main(port=8000):
    # Parse args
    args = parse_args()

    # Open a window
    if args.browser:
        webbrowser.open("http://localhost:{}".format(port))

    # Begin the server
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
