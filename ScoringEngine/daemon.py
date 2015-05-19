"""
This script runs the ScoringEngine application using a development server.
"""

# We did not loose the bug!!!!!!!!!!
'''
       / .'
 .---. \/
(._.' \()
 ^"""^"
bug
'''

import ScoringEngine
import os

#!/usr/bin/python
import time
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/scoring/scoring.log'
        self.stderr_path = '/dev/log/scoring/scoring.err'
        self.pidfile_path =  '/tmp/scoring.pid'
        self.pidfile_timeout = 5
    def run(self):
        ScoringEngine.main()



if __name__ == '__main__':
    app = App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()
