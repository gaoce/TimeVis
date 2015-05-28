#!/usr/bin/env python
from flask import Flask

app = Flask('timevis')
app.config.from_object('timevis.config')
