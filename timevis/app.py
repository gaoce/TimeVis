#!/usr/bin/env python
from flask import Flask
import webbrowser
import argparse

# app = Flask('timevis')
app = Flask('timevis')


def parse_args():
    args = {}
    parser = argparse.ArgumentParser(description='TimeVis')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='Enable browser')
    args = parser.parse_args()

    return args


def main(port=8000):
    # Parse args
    args = parse_args()

    # Open a window
    if args.browser:
        webbrowser.open("http://localhost:{}/".format(port), new=2)

    # Begin the server
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
    main()
