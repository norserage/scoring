#!/usr/bin/python
from flup.server.fcgi import WSGIServer
import ScoringEngine
import ScoringEngine.conf
from ScoringEngine.web import app

if __name__ == '__main__':
	ScoringEngine.conf.loadConf(config, env)
	WSGIServer(app, bindAddress='/tmp/scoring.sock').run()