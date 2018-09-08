"""
Copyright 2016 Brandon Warner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import print_function
VERSION = '3.2'
VERSIONSTR = "Lepus ISE v%s DEV" % (VERSION)
'''

'''



def arguments():
    import ScoringEngine.core.conf
    import argparse
    parser = argparse.ArgumentParser(description=VERSIONSTR)
    parser.add_argument('-e','--env', help='Environment', required=False)
    parser.add_argument('-c','--config', help='Specify the config file', required=False)
    parser.add_argument('--gen-config', help='Generates a new default config file', required=False, action='store_true')
    parser.add_argument('--gen-db', help='Imports the schema into a database', required=False, action='store_true')
    parser.add_argument('--print-config', help='Prints the current configuration', required=False, action='store_true')
    parser.add_argument('-v','--version', help='Generates a new default config file', required=False, action='store_true')
    
    args = parser.parse_args()

    env = None

    config = 'conf.yaml'
    if args.config:
        config = args.config

    if args.version:
        print(VERSIONSTR)
        return False
    elif args.gen_config:
        ScoringEngine.core.conf.newConf(config)
        return False
    elif args.env:
        env = args.env

    ScoringEngine.core.conf.loadConf(config, env)

    if args.print_config:
        import pprint
        print("")
        pprint.pprint(ScoringEngine.core.conf.conf)

    if args.gen_db:
        import ScoringEngine.core.db
        import ScoringEngine.core.db.tables
        ScoringEngine.core.db.tables.Base.metadata.create_all(ScoringEngine.core.db.engine)
        ScoringEngine.core.db.createUser("Administrator", "admin", "admin", -1, 5)
        return False

    
    return True

def pathSetup():
    from ScoringEngine.core.conf import conf
    import sys
    if 'tester locations' in conf:
        if len(conf['tester locations']) > 0:
            for l in conf['tester locations']:
                sys.path.append(l)

def main():
    if arguments():
        from ScoringEngine.core.conf import conf
        from os import environ
        from ScoringEngine.web import app, setupApp
        HOST = environ.get('SERVER_HOST', conf['listen'])
        try:
            PORT = int(environ.get('SERVER_PORT', str(conf['port'])))
        except ValueError:
            PORT = conf['port']
        pathSetup()
        #engine.start() # Note that this starts a thread
        setupApp()
        app.run(HOST, PORT)
        print("hello")

def fcgimain():
    if arguments():
        from ScoringEngine.core.conf import conf
        from ScoringEngine.web import app, setupApp
        from flup.server.fcgi import WSGIServer
        pathSetup()
        setupApp()
        WSGIServer(app, bindAddress=conf['fcgi']['socket']).run()