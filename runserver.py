"""
This script runs the teamportal application using a development server.
"""

from os import environ
from teamportal import app
UPLOAD_FOLDER = './static/uploads'
#
#app.secret_key = 'super_secret_key_230742'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#------------------------- App Launch ------------------------------------
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')    
    #app.debug = True
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
