#!/usr/bin/python
from flup.server.fcgi import WSGIServer
import ScoringEngine
import ScoringEngine.conf

if __name__ == '__main__':
	ScoringEngine.conf.loadConf()
	from ScoringEngine.web import app
	WSGIServer(app, bindAddress='/tmp/scoring.sock').run()