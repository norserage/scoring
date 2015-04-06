#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from ScoringEngine import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/tmp/scoring.sock').run()