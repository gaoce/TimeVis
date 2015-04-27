#!/usr/bin/env python
from flask import Flask

app = Flask('timevis')


def main():
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
    main()
