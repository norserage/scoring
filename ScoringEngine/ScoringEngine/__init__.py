﻿from __future__ import print_function
VERSION = '2.6'
VERSIONSTR = "Lepus ISE v%s DEV" % (VERSION)
'''

'''



def arguments():
    import ScoringEngine.conf
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
        ScoringEngine.conf.newConf(config)
        return False
    elif args.env:
        env = args.env

    ScoringEngine.conf.loadConf(config, env)

    if args.print_config:
        import pprint
        print("")
        pprint.pprint(ScoringEngine.conf.conf)

    if args.gen_db:
        import ScoringEngine.db
        import ScoringEngine.db.tables
        ScoringEngine.db.tables.Base.metadata.create_all(ScoringEngine.db.engine)
        ScoringEngine.db.createUser("Administrator", "admin", "admin", -1, 5)
        return False

    
    return True

def pathSetup():
    from ScoringEngine.conf import conf
    import sys
    if 'tester locations' in conf:
        if len(conf['tester locations']) > 0:
            for l in conf['tester locations']:
                sys.path.append(l)

def main():
    if arguments():
        from ScoringEngine.conf import conf
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
        from ScoringEngine.conf import conf
        from ScoringEngine.web import app, setupApp
        from flup.server.fcgi import WSGIServer
        pathSetup()
        setupApp()
        WSGIServer(app, bindAddress=conf['fcgi']['socket']).run()