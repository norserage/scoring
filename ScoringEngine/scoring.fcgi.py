#!/usr/bin/python
from flup.server.fcgi import WSGIServer
import ScoringEngine
import ScoringEngine.conf

if __name__ == '__main__':
	ScoringEngine.fcgimain()
