#!/usr/bin/env python3.6

from flask import Flask
from app.views import view

app = Flask(__name__)
app.register_blueprint(view)

app.run(debug=False, host="0.0.0.0")
