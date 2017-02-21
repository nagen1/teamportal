"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
app.secret_key = 'super_secret_key_230742'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

import teamportal.views
