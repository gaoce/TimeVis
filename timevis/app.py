#!/usr/bin/env python
from flask import Flask
import os

app = Flask('timevis')
app.config.from_object('timevis.config')

if os.environ.get('TIMEVIS_CONFIG') is not None:
    app.config.from_envvar('TIMEVIS_CONFIG')
