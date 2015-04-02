"""
This script runs the ScoringEngine application using a development server.
"""
import sys
sys.path.append("testers/")
# Note we did not loose the bug
'''
       / .'
 .---. \/
(._.' \()
 ^"""^"
bug
'''
from os import environ
from ScoringEngine import app
#from ScoringEngine import engine
import ScoringEngine.conf
from ScoringEngine.conf import conf
import argparse

if __name__ == '__main__':



    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #engine.start() # Note that this starts a thread
    app.debug = True
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(HOST, PORT)
